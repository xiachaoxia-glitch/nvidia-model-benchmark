#!/usr/bin/env python3
"""
NVIDIA NIM LLM Speed & Latency Benchmark Tool
Measures Time-to-First-Token (TTFT), Total Generation Time, and Tokens Per Second (TPS).
"""
import os
import sys
import time
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List

API_KEY = os.getenv("NVIDIA_API_KEY", "")
API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

DEFAULT_MODELS = [
    "meta/llama-3.1-70b-instruct",
    "meta/llama-3.1-8b-instruct",
    "meta/llama-3.3-70b-instruct",
    "mistralai/mixtral-8x7b-instruct-v0.1",
    "mistralai/mixtral-8x22b-instruct-v0.1",
    "qwen/qwen2.5-72b-instruct",
    "qwen/qwen2.5-coder-32b-instruct",
    "deepseek-ai/deepseek-r1",
]

TEST_PROMPT = [
    {"role": "user", "content": "Write exactly 3 short sentences about artificial intelligence and space exploration."}
]


def test_model(model_id: str, api_key: str) -> Dict[str, Any]:
    """Test streaming latency and speed for a model"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model_id,
        "messages": TEST_PROMPT,
        "max_tokens": 120,
        "temperature": 0.1,
        "stream": True,
    }

    req = urllib.request.Request(API_URL, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    t0 = time.time()
    first_token_time = None
    token_count = 0
    collected_text = ""

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            for line in resp:
                line_str = line.decode("utf-8", errors="replace").strip()
                if line_str.startswith("data: ") and line_str != "data: [DONE]":
                    if first_token_time is None:
                        first_token_time = time.time()
                    token_count += 1
                    try:
                        chunk = json.loads(line_str[6:])
                        delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        collected_text += delta
                    except Exception:
                        pass
        t_end = time.time()
        ttft = (first_token_time - t0) if first_token_time else (t_end - t0)
        total_time = t_end - t0
        gen_time = (t_end - first_token_time) if first_token_time else total_time
        tps = token_count / gen_time if gen_time > 0 else 0

        return {
            "model": model_id,
            "status": "OK",
            "ttft_s": round(ttft, 3),
            "total_time_s": round(total_time, 3),
            "tokens": token_count,
            "tps": round(tps, 2),
            "preview": collected_text.replace("\n", " ")[:60],
        }
    except Exception as e:
        return {
            "model": model_id,
            "status": f"Error: {str(e)[:50]}",
            "ttft_s": 0,
            "total_time_s": 0,
            "tokens": 0,
            "tps": 0,
            "preview": "",
        }


def main():
    api_key = API_KEY or os.getenv("NVIDIA_API_KEY", "")
    if not api_key:
        print("❌ Error: NVIDIA_API_KEY environment variable not found.", file=sys.stderr)
        print("Please set your API key: export NVIDIA_API_KEY='nvapi-...'")
        sys.exit(1)

    models_to_test = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_MODELS

    print(f"Testing {len(models_to_test)} NVIDIA NIM models...\n")
    print(f"{'Model':<40} | {'Status':<10} | {'TTFT(s)':<8} | {'Total(s)':<8} | {'Tokens/s':<8} | {'Tokens'}")
    print("-" * 90)

    results = []
    for m in models_to_test:
        res = test_model(m, api_key)
        results.append(res)
        print(f"{res['model']:<40} | {res['status']:<10} | {res['ttft_s']:<8} | {res['total_time_s']:<8} | {res['tps']:<8} | {res['tokens']}")

    print("\nBenchmark completed.")


if __name__ == "__main__":
    main()
