# NVIDIA NIM Model Benchmark Suite

Comprehensive benchmarking toolkit for evaluating NVIDIA NIM hosted Large Language Models (LLMs) and Vision-Language Models (VLMs).

## Metrics Measured

- ⏱️ **Time to First Token (TTFT)**: Initial latency until the first streamed chunk arrives.
- ⚡ **Tokens Per Second (TPS)**: Effective decoding and streaming throughput.
- 🕒 **Total End-to-End Latency**: Complete roundtrip execution time.
- 🖼️ **Multimodal / Vision Response Speed**: Image upload and VLM inference time.

## Quick Start

### 1. Requirements
```bash
pip install -r requirements.txt
```

### 2. Set Your NVIDIA API Key
Get your free API key at [build.nvidia.com](https://build.nvidia.com/):
```bash
export NVIDIA_API_KEY="nvapi-..."
# Or in Windows PowerShell:
$env:NVIDIA_API_KEY="nvapi-..."
```

### 3. Run LLM Speed Benchmark
```bash
python benchmark_llm.py
```

### 4. Run Multimodal Vision Benchmark
```bash
python benchmark_vision.py
```

## License
MIT License
