# 为什么这样写：3. Method

方法章写真实流程：候选选题、评审选择、多 agent 写作、85 分返修、imagegen 图像路径。它回应用户要求：不是硬编码 prompt，而是从素材出发再循环写作。

## 迭代说明

- 第一轮：确定本节回答的 reader question。
- 第二轮：检查是否有 unsupported claim。
- 第三轮：把批评转成修订或 caveat。
- 通过条件：本节不把 demo/synthetic 内容写成真实实证结论。
