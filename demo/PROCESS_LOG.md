# Demo process log / 可复现过程记录

## 生成方式

Deterministic local generation. This log intentionally does not include wall-clock time so repeated runs can produce stable content.

## 输入

- 文件：`demo/input_material.md`
- SHA256：`4799f0bfd52dac6da509e0363e92a4a3978e9727f8de279c8d16494b19f3b2b5`
- 主题：PPO 与强化学习评测
- 输入类型：公开知识型素材 + 用户指定的 demo 任务

## 操作步骤

1. 读取 `input_material.md`。
2. 识别论文类型：benchmark / evaluation paper。
3. 提取核心冲突：average return 可能高估真实 policy reliability。
4. 构造论文主张：Policy-MME 用层级能力和组级评分诊断 PPO 类算法。
5. 按章节执行契约、段落计划、草稿、批评、修订和 rationale 的多轮流程。
6. 生成 `paper.md` 的长文正文。
7. 生成 `explain/why_each_section.md`，逐章解释写作理由。
8. 生成 `WORKFLOW_PLAN.md` 和 `ITERATION_LOG.md`，记录稳定可复现的流程。
9. 从正文 claim 生成 `figures/figure_prompts.md` 和 `figures/IMAGEGEN_PROCESS.md`，供 Codex imagegen 生成位图。
10. 生成 SVG preview，仅作为确定性结构预览。
11. 写出 `MANIFEST.md`，记录所有输出文件哈希。

## 可复现命令

```bash
uv run python demo/run_demo.py
```

如果要验证可复现性，可以删除以下文件后重新运行：

```bash
rm -f demo/paper.md demo/PROCESS_LOG.md demo/MANIFEST.md
rm -f demo/explain/why_each_section.md
rm -f demo/figures/figure1_pipeline.svg demo/figures/figure2_results.svg demo/figures/figure_prompts.md
uv run python demo/run_demo.py
```

## 诚信边界

- 本 demo 不调用真实 RL 环境。
- 所有实验数值都是 synthetic placeholders。
- 图 2 是演示图，不是实验结果证明。
- SVG 是 deterministic preview，不是默认最终生图路径。
- 真正生图应使用 Codex imagegen，并保留 prompt 与 audit。
- 系统必须解释为什么这么写，不能只输出漂亮正文。
