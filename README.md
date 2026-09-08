# NVIDIA Model Benchmark Suite ⚡

> **Speed, TTFT Latency, and Throughput Benchmark Suite for NVIDIA NIM LLM & Vision Models**
> 针对 NVIDIA NIM 微服务、托管 API（包括 LLM 与多模态视觉模型）的专业测速、首字延迟（TTFT）与高并发吞吐压测工具。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)]()
[![Zero-Dependency](https://img.shields.io/badge/Dependencies-Standard%20Library%20Only-success.svg)]()

---

## 🌟 核心特性 (Features)

- ⏱️ **毫秒级时延监控**：精确计算首字生成延迟（Time-To-First-Token, TTFT）与端到端传输延迟。
- 📊 **吞吐量与生成速度 (TPS)**：实时统计每秒 Token 输出速率（Tokens Per Second），全面反映实际流式生成体验。
- 🚀 **并发压测 (Concurrency Stress Test)**：支持多并发客户端模拟（并发数、总请求量自定义），输出 P50/P90 延迟分位数与集群吞吐。
- 👁️ **多模态视觉评测 (Vision NIM Support)**：内置针对 VLM（如 NV-Embed / Phi-4-Multimodal 等）的多模态图文推理基准。
- 零外部强制依赖：核心基准测试工具仅基于 Python 原生标准库（`urllib`, `concurrent.futures`, `json`），开箱即用，无需繁琐安装。

---

## 🚀 快速开始 (Quick Start)

### 1. 配置 API 密钥

获取 NVIDIA API Key 并设置为环境变量：

```bash
# Windows PowerShell
$env:NVIDIA_API_KEY="nvapi-xxxxxx"

# Linux / macOS / Git Bash
export NVIDIA_API_KEY="nvapi-xxxxxx"
```

### 2. 执行基准评测

#### 🔹 基础模型测速 (单请求流式 TTFT 与 TPS 测量)
```bash
python benchmark_llm.py
```
*自动测试预设的主流模型梯队（Llama-3.1, Mixtral, Qwen2.5, DeepSeek-R1 等），并输出排列表格。*

#### 🔹 高并发吞吐压测 (模拟多并发工作负载)
```bash
python benchmark_concurrent.py --model meta/llama-3.1-8b-instruct -c 4 -n 16
```
参数说明：
- `-c, --concurrency`：并发客户端线程数（例如 4、8、16）
- `-n, --requests`：总请求数（例如 16、32、100）
- `--model`：测试的目标模型全名

输出示例：
```text
Concurrency Benchmark Summary for meta/llama-3.1-8b-instruct
Success Rate: 16/16 (100.0%)
Total Wall Clock Time: 4.82s
Average TTFT: 620.4 ms (Min: 512ms, Max: 780ms)
Average Request Latency: 1140.2 ms
P50 Latency: 1120.0 ms
P90 Latency: 1350.0 ms
Effective Aggregate Throughput: 142.30 tokens/sec
```

#### 🔹 多模态视觉模型测速 (Vision & OCR Benchmark)
```bash
python benchmark_vision.py --image path/to/sample.jpg
```

---

## 📈 实测选型参考 (Field Benchmark Highlights)

基于最新实测数据提炼的部分典型模型表现（完整报告请阅读 [Field Benchmark Report](docs/benchmark_report.md)）：

| 模型 (Model) | 平均响应 (ms) | 首字生成体验 | 生成速度 (Tok/s) | 适合场景 |
| :--- | :---: | :---: | :---: | :--- |
| `mistralai/mistral-nemotron` | **682 ms** | 极速 | 8.31 | 交互式 Agent、实时对话 |
| `mistralai/mixtral-8x7b` | **1147 ms** | 迅速 | **13.95** | 高并发生产业务 |
| `stepfun-ai/step-3.7-flash` | **1882 ms** | 稳定 | 8.50 | 结构化信息提炼 |
| `deepseek-ai/deepseek-v4-pro` | **3568 ms** | 较长 | - | 复杂长推理与深度编码 |

---

## 🛠️ GitHub Actions 集成

本项目已内置 `.github/workflows/ci.yml`，每次提交自动校验代码语法规范与模块兼容性。

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 协议开源。
