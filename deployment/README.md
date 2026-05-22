# Deployment

部署配置目录，由 E 块维护。

当前包含：

- `docker-compose.yml`：后端 API 容器启动配置

当前 Docker 构建以上级项目根目录为上下文，因此容器内会包含：

- `backend/`
- `frontend/`
- `data/`
- `models/`

这样 `/dashboard`、真实数据和模型产物在容器中都可以被后端读取。

后续可扩展：

- Nginx 反向代理配置
- 前端静态资源部署配置
- 生产环境环境变量模板
