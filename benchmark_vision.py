#!/usr/bin/env python3
"""
NVIDIA NIM Multimodal Vision Models Benchmark
Tests Vision Language Model (VLM) image understanding speed, latency, and response quality.
"""
import os
import sys
import time
import json
import base64
import io
import requests
from PIL import Image

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
API_KEY = os.getenv("NVIDIA_API_KEY", "")

VISION_MODELS = [
    "meta/llama-3.2-11b-vision-instruct",
    "meta/llama-3.2-90b-vision-instruct",
    "google/deplot",
    "nvidia/neva-22b",
]


def generate_sample_image_b64() -> str:
    """Generate a test in-memory PNG image"""
    img = Image.new("RGB", (200, 200), color=(73, 109, 137))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def benchmark_vlm(model: str, img_b64: str, api_key: str):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the main color and shape in this image in one brief sentence."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                ]
            }
        ],
        "max_tokens": 60,
        "temperature": 0.2
    }

    t0 = time.time()
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        elapsed = time.time() - t0
        if resp.status_code == 200:
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            tokens = usage.get("completion_tokens", 0)
            return {"status": "OK", "time_s": round(elapsed, 2), "tokens": tokens, "reply": content.strip()[:60]}
        else:
            return {"status": f"HTTP {resp.status_code}", "time_s": round(elapsed, 2), "tokens": 0, "reply": resp.text[:50]}
    except Exception as e:
        return {"status": "Error", "time_s": 0, "tokens": 0, "reply": str(e)[:50]}


def main():
    api_key = API_KEY or os.getenv("NVIDIA_API_KEY", "")
    if not api_key:
        print("❌ Error: NVIDIA_API_KEY environment variable not found.", file=sys.stderr)
        sys.exit(1)

    print("Generating synthetic image for VLM benchmark...")
    img_b64 = generate_sample_image_b64()

    print(f"\nBenchmarking {len(VISION_MODELS)} Multimodal Vision Models...")
    print(f"{'Model':<40} | {'Status':<10} | {'Latency(s)':<10} | {'Tokens':<8} | {'Output'}")
    print("-" * 90)

    for m in VISION_MODELS:
        res = benchmark_vlm(m, img_b64, api_key)
        print(f"{m:<40} | {res['status']:<10} | {res['time_s']:<10} | {res['tokens']:<8} | {res['reply']}")

if __name__ == "__main__":
    main()
