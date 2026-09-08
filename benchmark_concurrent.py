#!/usr/bin/env python3
"""
NVIDIA NIM Concurrency & Throughput Stress Benchmark Tool
Evaluates server response time, TTFT, and total TPS under concurrent load (1-32 concurrent workers).
"""
import os
import sys
import time
import json
import argparse
import statistics
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List

API_KEY = os.getenv("NVIDIA_API_KEY", "")
API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

PROMPT = [
    {"role": "user", "content": "Explain the concept of quantum computing in exactly two sentences."}
]


def send_single_request(model_id: str, api_key: str, max_tokens: int = 80, timeout: int = 60) -> Dict[str, Any]:
    """Execute one streaming request and gather timing metrics."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model_id,
        "messages": PROMPT,
        "max_tokens": max_tokens,
        "temperature": 0.1,
        "stream": True,
    }

    req = urllib.request.Request(API_URL, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    t0 = time.time()
    first_token_time = None
    tokens = 0
    err_msg = None

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            for line in resp:
                decoded = line.decode("utf-8", errors="replace").strip()
                if decoded.startswith("data: ") and decoded != "data: [DONE]":
                    if first_token_time is None:
                        first_token_time = time.time()
                    tokens += 1
        t_end = time.time()
        ttft = (first_token_time - t0) if first_token_time else (t_end - t0)
        total_time = t_end - t0
        gen_time = (t_end - first_token_time) if first_token_time else total_time
        tps = (tokens / gen_time) if gen_time > 0 and tokens > 0 else 0.0

        return {
            "success": True,
            "ttft_ms": round(ttft * 1000, 1),
            "total_ms": round(total_time * 1000, 1),
            "tokens": tokens,
            "tps": round(tps, 2),
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "ttft_ms": 0.0,
            "total_ms": round((time.time() - t0) * 1000, 1),
            "tokens": 0,
            "tps": 0.0,
            "error": str(e)
        }


def run_concurrency_test(model: str, concurrency: int, total_requests: int, api_key: str):
    print(f"\n[🚀 Benchmark] Testing model: {model}")
    print(f"Concurrency: {concurrency} workers | Total Requests: {total_requests}")
    print("-" * 65)

    start_bench = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(send_single_request, model, api_key) for _ in range(total_requests)]
        for f in as_completed(futures):
            res = f.result()
            results.append(res)
            status = "✓" if res["success"] else "✗"
            print(f" {status} req finished in {res['total_ms']}ms (TTFT: {res['ttft_ms']}ms, TPS: {res['tps']})")

    total_wall_time = time.time() - start_bench
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print("=" * 65)
    print(f"Concurrency Benchmark Summary for {model}")
    print(f"Success Rate: {len(successful)}/{total_requests} ({len(successful)/total_requests*100:.1f}%)")
    print(f"Total Wall Clock Time: {total_wall_time:.2f}s")

    if successful:
        ttfts = [r["ttft_ms"] for r in successful]
        latencies = [r["total_ms"] for r in successful]
        total_tokens = sum(r["tokens"] for r in successful)
        cluster_tps = total_tokens / total_wall_time

        print(f"Average TTFT: {statistics.mean(ttfts):.1f} ms (Min: {min(ttfts)}ms, Max: {max(ttfts)}ms)")
        print(f"Average Request Latency: {statistics.mean(latencies):.1f} ms")
        if len(latencies) >= 2:
            print(f"P50 Latency: {statistics.median(latencies):.1f} ms")
            print(f"P90 Latency: {statistics.quantiles(latencies, n=10)[8]:.1f} ms")
        print(f"Total Tokens Generated: {total_tokens}")
        print(f"Effective Aggregate Throughput: {cluster_tps:.2f} tokens/sec")

    if failed:
        print(f"[!] Failures ({len(failed)}):")
        for f in failed[:3]:
            print(f"   - {f['error']}")


def main():
    parser = argparse.ArgumentParser(description="NVIDIA NIM Concurrency & Load Benchmark")
    parser.add_argument("--model", type=str, default="meta/llama-3.1-8b-instruct",
                        help="NVIDIA model identifier")
    parser.add_argument("--concurrency", "-c", type=int, default=4,
                        help="Number of concurrent client workers")
    parser.add_argument("--requests", "-n", type=int, default=8,
                        help="Total number of requests to execute")
    parser.add_argument("--api-key", type=str, default=API_KEY,
                        help="NVIDIA API key (or set NVIDIA_API_KEY env var)")
    args = parser.parse_args()

    if not args.api_key:
        print("Error: NVIDIA API Key is required. Set NVIDIA_API_KEY or use --api-key.")
        sys.exit(1)

    run_concurrency_test(args.model, args.concurrency, args.requests, args.api_key)


if __name__ == "__main__":
    main()
