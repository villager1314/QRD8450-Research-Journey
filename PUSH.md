# 本地使用与推送

当前仓库已配置 origin：`https://github.com/villager1314/QRD8450-Research-Journey.git`。已有仓库的 clone 和日常流程见下文。

## 首次创建远程仓库（仅适用于新项目）

以下为最初无远程地址的 ZIP 分发流程，不用于重新初始化当前仓库。

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

早期 ZIP 的初始提交使用局部占位身份 Research Notes / research-notes@example.invalid。日常提交应配置自己的 Git 身份；当前已有共享历史时，不为更换身份改写旧提交。

## 已有远程仓库：clone

现有仓库地址如下。在准备存放副本的父目录执行，勿在已有工作目录内重复 clone：

```bash
git clone https://github.com/villager1314/QRD8450-Research-Journey.git
cd QRD8450-Research-Journey
git status
git remote -v
```

已有本地仓库直接进入目录使用，无需重新初始化或覆盖 .git。上文“首次创建空仓库”流程仅适用于尚未建立远程的新项目，不用于当前仓库。

## 日常更新、提交和推送

先检查工作区；有未提交改动时先整理保存，再执行拉取，避免混入其他工作。工作区干净时可快进更新：

```bash
git status
git pull --ff-only
```

修改后先审阅差异、检查文档链接，再按需选择文件暂存：

```bash
git diff
git diff --check
git add README.md REFERENCES.md PUSH.md docs/boot/README.md docs/modules/README.md docs/journal/README.md
git diff --cached
git commit -m "Update QRD8450 research evidence"
git push
```

按本次实际修改调整 git add 列表；不要暂存固件、完整私人日志或凭据。若当前分支尚未设置上游，先用 `git branch --show-current` 确认分支；main 分支可执行 `git push -u origin main`。推送被拒绝时先 fetch 并审阅分歧，不强制推送。上述均为供用户手动执行的方法，本轮维护不自动提交或推送。
