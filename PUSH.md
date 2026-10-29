# 本地使用与推送

解压后进入 QRD8450-Research-Journey。ZIP 含本地 .git 和初始提交，无远程地址。

```bash
git status
git log --oneline -1
git remote add origin https://github.com/YOUR_USERNAME/QRD8450-Research-Journey.git
git push -u origin main
```

请先在 GitHub 创建同名空仓库，不预建 README。认证使用你自己的凭据，不要把令牌写进仓库或 URL。

若解压工具未保留 .git，可重新初始化：

```bash
git init -b main
git add .
git commit -m "Initialize QRD8450 research notes"
```

首次提交使用仓库局部占位身份 Research Notes / research-notes@example.invalid。你可以配置自己的身份，再用 `git commit --amend --reset-author --no-edit` 更新初始提交作者。
