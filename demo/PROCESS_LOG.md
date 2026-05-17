# Demo process log / 可复现过程记录

## 生成方式

Deterministic local generation. This log intentionally does not include wall-clock time so repeated runs can produce stable content.

## 输入

- 文件：`demo/input_material.md`
- SHA256：`2093dc3c70d1c592d9cf5fe825771991f97aacdb1c78c33b606914a016a8b257`
- 主题：PPO 与强化学习评测
- 输入类型：公开知识型素材 + 用户指定的 demo 任务

## 操作步骤

1. 读取 `input_material.md`。
2. 识别论文类型：benchmark / evaluation paper。
3. 提取核心冲突：average return 可能高估真实 policy reliability。
4. 构造论文主张：Policy-MME 用层级能力和组级评分诊断 PPO 类算法。
5. 生成 `paper.md` 的 8 个章节。
6. 生成 `explain/why_each_section.md`，逐章解释写作理由。
7. 生成两张可复现 SVG 图：pipeline overview 和 synthetic score comparison。
8. 生成 `figures/figure_prompts.md`，供 image2 / imagegen 生成位图版本。
9. 写出 `MANIFEST.md`，记录所有输出文件哈希。

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
- 系统必须解释为什么这么写，不能只输出漂亮正文。
