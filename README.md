# 基于协同过滤的美食推荐系统的设计与实现

> Django + 协同过滤算法的美食推荐系统。

本项目由 [HRouter](https://hrouter.net) 赞助 —— 面向开发者的 AI 中转站：一个 Key 调用多家大模型，稳定透明，注册即用。

## 文档与资源

- [开发文档](docs/thesis/README.md)：Markdown 图文格式，GitHub 上直接阅读。
- [PlantUML 图源](docs/diagrams/)：共 7 个文件（`.plantuml` / `.puml` / `.wsd`）。
- [数据库初始化说明](database/README.md)

## 源码目录

- `Food-Recommend-System/`

## 本地运行准备

1. 根据项目中的依赖声明安装对应语言运行时和数据库。
2. 查看下方依赖入口及初始化说明，按实际模块分别安装依赖。
3. 搜索 `CHANGE_ME_BEFORE_RUNNING`，填入自己的本地配置；不要提交真实密码、令牌和第三方服务密钥。
4. 启动相应后端，再启动前端或在小程序开发工具中导入客户端。

以下命令依据现有文件列出，**不代表已完成全项目安装、联调或运行验证**。

### Django 初始化

在 `Food-Recommend-System/` 配置好数据库后执行：

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 第三方组件与许可

现有第三方组件的 LICENSE、NOTICE 和作者声明保留原样；本项目不替换原有许可，也不额外声明所有代码适用同一开源许可证。
