# NVIDIA NIM Model Benchmark Field Report

Comprehensive evaluation of latency, streaming TTFT (Time-to-First-Token), and generation throughput across popular NVIDIA NIM endpoints.

---

## 📊 Summary of Probed Models (Latency & Throughput Ranking)

*Test conditions: NVIDIA Integrate API, 3 samples per model, max concurrency = 2~4.*

| Rank | Model Identifier | Parameter Scale / Arch | TTFT / Avg Latency (ms) | Peak Throughput (Tokens/s) | Success Rate | Recommendation |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | `mistralai/mistral-small-4-119b-2603` | 119B MoE | **588 ms** | 5.67 | 100% | ⚡ Ultra-fast general response |
| **2** | `mistralai/mistral-nemotron` | Specialized | **682 ms** | 8.31 | 100% | ⚡ High TPS & low latency |
| **3** | `moonshotai/kimi-k2.6` | Large LM | **776 ms** | 2.58 | 100% | 🎯 Very consistent response time |
| **4** | `google/gemma-4-31b-it` | 31B Dense | **812 ms** | 2.46 | 100% | 🎯 Stable general assistant |
| **5** | `sarvamai/sarvam-m` | Medium | **979 ms** | **16.34** | 100% | 🚀 Highest single-stream TPS |
| **6** | `mistralai/mixtral-8x7b-instruct-v0.1` | 8x7B MoE | **1147 ms** | **13.95** | 100% | 🚀 High throughput production tier |
| **7** | `openai/gpt-oss-20b` | 20B Dense | **1441 ms** | **11.11** | 100% | 🌟 Smooth streaming experience |
| **8** | `stepfun-ai/step-3.7-flash` | Lightweight | **1882 ms** | 8.50 | 100% | Balanced flash model |
| **9** | `stepfun-ai/step-3.5-flash` | Lightweight | **3164 ms** | 5.06 | 100% | Standard light model |
| **10** | `deepseek-ai/deepseek-v4-pro` | Flagship MoE | **3568 ms** | 0.56 | 100% | 🧠 Deep reasoning capability |
| **11** | `meta/llama-3.1-8b-instruct` | 8B Dense | **6733 ms** | 0.40 | 100% | Edge-compatible baseline |
| **12** | `meta/llama-3.1-70b-instruct` | 70B Dense | **9074 ms** | 0.22 | 100% | Comprehensive enterprise scale |

---

## 🎯 Key Takeaways & Selection Advice

1. **For Real-Time Interactive / Streaming Agent Workloads**:
   - Prefer `mistralai/mistral-nemotron` or `mistralai/mixtral-8x7b-instruct-v0.1`.
   - Sub-second first-token latency with sustained 10~16 tokens/sec generation speed.
2. **For High-Concurrency Multi-tenant Scenarios**:
   - Use `benchmark_concurrent.py` to evaluate your specific token budget and rate-limits before scaling up.
3. **For Large-Scale Reasoning & Analytics**:
   - `deepseek-ai` and `meta/llama-3.1-70b` deliver superior reasoning depth but require generous client timeouts (>60s).
