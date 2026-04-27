# 部署说明

## 1. 后端本地开发部署

在项目根目录执行：

```bash
cd backend/player-profiling-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

服务默认运行在：

```text
http://127.0.0.1:8000
```

## 2. 后端生产方式启动

```bash
cd backend/player-profiling-api
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 3. Docker Compose 部署

在项目根目录执行：

```bash
docker compose -f deployment/docker-compose.yml up --build
```

## 4. 单独构建后端镜像

```bash
cd backend/player-profiling-api
docker build -t player-profiling-api .
docker run -p 8000:8000 player-profiling-api
```

## 5. Nginx 反向代理示例

```nginx
server {
    listen 80;
    server_name example.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 6. 上线前检查

- `/api/v1/health` 正常返回
- `/docs` 可以打开
- 前端请求地址已切换为部署域名
- `.env`、虚拟环境、缓存文件没有提交到 GitHub
- 根目录 README 中的启动命令可以复现
