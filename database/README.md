# 数据库初始化说明

本仓库不包含原始用户、账号密码、订单、联系方式和业务数据快照。

本项目保留 Django 模型及迁移文件。配置数据库后运行 `python manage.py migrate`，再按需执行 `python manage.py createsuperuser`。

真实连接信息已替换为本地地址或占位值，运行前请按实际环境填写。
