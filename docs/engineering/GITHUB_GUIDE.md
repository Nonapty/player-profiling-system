# GitHub 上传与协作指南

以下步骤适合第一次使用 GitHub 的小组项目。

## 1. 在 GitHub 新建整体项目仓库

1. 打开 GitHub
2. 点击右上角 `+`
3. 选择 `New repository`
4. 仓库名建议：`player-profiling-system`
5. 不要勾选 README、`.gitignore`、license，因为本地已经有这些文件
6. 点击 `Create repository`

## 2. 本地初始化 Git

在项目根目录执行：

```bash
git init
git add .
git commit -m "Initial team project structure"
```

## 3. 连接远程仓库

把下面地址替换成你自己的 GitHub 仓库地址：

```bash
git remote add origin https://github.com/你的用户名/player-profiling-system.git
git branch -M main
git push -u origin main
```

## 4. 后续日常提交

每次修改后执行：

```bash
git status
git add .
git commit -m "描述本次修改"
git push
```

## 5. 和组员协作

组员第一次下载项目：

```bash
git clone https://github.com/你的用户名/player-profiling-system.git
cd player-profiling-system
```

每次开始写代码前先拉取最新版本：

```bash
git pull
```

再修改、提交、推送。

## 6. 推荐协作方式

小组项目早期可以直接推送到 `main`，但更推荐每个人建自己的分支：

```bash
git checkout -b feature/你的模块名
```

例如：

```bash
git checkout -b feature/frontend-dashboard
git checkout -b feature/ml-analytics
git checkout -b feature/data-pipeline
```

完成后推送分支：

```bash
git push -u origin feature/你的模块名
```

然后在 GitHub 页面发起 Pull Request。

## 7. 常见问题

### 提示没有登录权限

可以使用 GitHub CLI 登录：

```bash
gh auth login
```

也可以使用 GitHub 网页生成 Personal Access Token。

### 不小心把虚拟环境加进去了

确认 `.gitignore` 包含 `.venv/`，然后执行：

```bash
git rm -r --cached backend/player-profiling-api/.venv
git commit -m "Remove virtual environment from git"
git push
```
