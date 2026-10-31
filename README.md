# Physical Archive

`pages/` 是 GitHub Pages 静态版，展示 arXiv 元数据并跳转原文；不包含投稿或评论。每个专题展示最新 100 条结果，摘要中含可访问的非空 GitHub 仓库链接的论文排在前面，搜索只覆盖这些数据。仓库许可与代码内容未核验，摘要中没有链接的项目可能无法显示代码入口。GitHub 接口出现限流或故障时更新失败，保留已发布版本。

## 部署
1. 将项目推送到 GitHub 仓库的 `main` 分支，不要上传 `community.db`。
2. 在仓库 Settings → Pages → Build and deployment → Source 选择 GitHub Actions。
3. 在 Actions 运行 Update and deploy Pages；工作流也会每日更新。数据获取失败时部署失败，已发布的旧版本保持不变。

本地生成数据：`python scripts/fetch_arxiv.py`。从 `pages` 目录运行 `python -m http.server 8001` 后访问 http://localhost:8001/。

社区投稿、评论需要独立后端，当前静态版不提供。上线前请核实适用的 arXiv 数据条款和当地法规。

