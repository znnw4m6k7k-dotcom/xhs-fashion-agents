# xhs-fashion-agents

本仓库提供女装小红书工作流使用的两个窄职责 Codex 自定义 Agent：

- `xiaohongshu-product-image-reviewer.toml`：独立审图，逐图输出 A/B/C 与一次性定向返工意见。
- `xiaohongshu-fact-copywriter.toml`：根据已验证事实、用户卖点和六张 A 图写标题、正文与标签。

两个 Agent 都不能审批、上传或发布。

使用完整工作流时，先安装并验证本仓库的两个 Agent，再安装 [xhs-fashion-qc-publish](https://github.com/znnw4m6k7k-dotcom/xhs-fashion-qc-publish)。

## 在 Codex 聊天窗口安装

把下面一整句话发送给 Codex：

```text
请打开 https://github.com/znnw4m6k7k-dotcom/xhs-fashion-agents ，完整阅读 README.md 和 AGENTS.md，运行仓库内 scripts/install_agents.py 安装两个 Codex 自定义 Agent；安装后运行 --check 验证，再读取 docs/使用说明-中文.md，并在当前聊天窗口给我一份完整中文说明书、两个 Agent 的安装路径、验证结果和首次调用示例。
```

安装器会写入 `${CODEX_HOME:-~/.codex}/agents/`。同内容会跳过；若同名文件内容不同，会先生成带时间戳的备份再更新，不会改动其他 Agent。

## 手动安装

```bash
git clone https://github.com/znnw4m6k7k-dotcom/xhs-fashion-agents.git
cd xhs-fashion-agents
python3 scripts/install_agents.py
python3 scripts/install_agents.py --check
```

安装后建议新开一个 Codex 对话，让 Agent 列表刷新。
