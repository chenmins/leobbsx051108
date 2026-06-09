# LeoBBS X Build051108 — 雷傲超级论坛

LeoBBS X 是 2005 年著名的中文社区论坛程序（雷傲超级论坛），基于 Perl CGI 开发，曾与 Discuz!、PHPWind 并列为中文互联网最流行的 BBS 程序之一。

本项目提供了 Docker 容器化方案，可一键部署运行。

---

## 快速开始

### 环境要求

- Docker 20.10+
- Docker Compose V2+

### 构建并启动

```bash
# 克隆代码
git clone https://github.com/chenmins/leobbsx051108.git
cd leobbsx051108

# 构建并后台启动
docker compose up -d --build
```

### 访问论坛

启动成功后，打开浏览器访问：

- **安装向导**：`http://localhost:8080/cgi-bin/install.cgi`
- **论坛首页**：`http://localhost:8080/cgi-bin/index.cgi`（安装完成后）

### 安装步骤

1. 访问 `http://localhost:8080/cgi-bin/install.cgi`
2. 第 1、2 项路径配置保持默认即可（程序会自动检测）
3. 设置管理员用户名和密码
4. 点击"开始安装"完成配置

---

## 常用命令

```bash
# 启动服务
docker compose up -d

# 停止服务
docker compose down

# 查看日志
docker compose logs -f

# 重新构建（修改代码后）
docker compose up -d --build

# 进入容器调试
docker exec -it leobbs-forum bash
```

---

## 数据持久化

以下目录通过 Docker Volume 持久化存储，容器重建后数据不会丢失：

| Volume 名称 | 容器内路径 | 说明 |
|---|---|---|
| `leobbs_data` | `/var/www/html/cgi-bin/data` | 论坛配置数据 |
| `leobbs_members` | `/var/www/html/cgi-bin/members` | 用户数据 |
| `leobbs_messages` | `/var/www/html/cgi-bin/messages` | 帖子/消息数据 |
| `leobbs_boarddata` | `/var/www/html/cgi-bin/boarddata` | 版块数据 |
| `leobbs_usr` | `/var/www/html/non-cgi/usr` | 用户上传文件 |

---

## 数据备份与恢复

### 备份

使用项目自带的备份脚本：

```bash
# 执行备份（备份文件保存到 ./backups/ 目录）
./backup.sh

# 指定备份目录
./backup.sh /path/to/backup/dir
```

备份文件命名格式：`leobbs_backup_YYYYMMDD_HHMMSS.tar.gz`

### 恢复

```bash
# 停止服务
docker compose down

# 解压备份文件到临时目录
mkdir -p /tmp/leobbs_restore
tar -xzf backups/leobbs_backup_XXXXXXXX_XXXXXX.tar.gz -C /tmp/leobbs_restore

# 恢复各 Volume 数据
docker run --rm -v leobbs_data:/data -v /tmp/leobbs_restore/data:/backup alpine sh -c "rm -rf /data/* && cp -a /backup/. /data/"
docker run --rm -v leobbs_members:/data -v /tmp/leobbs_restore/members:/backup alpine sh -c "rm -rf /data/* && cp -a /backup/. /data/"
docker run --rm -v leobbs_messages:/data -v /tmp/leobbs_restore/messages:/backup alpine sh -c "rm -rf /data/* && cp -a /backup/. /data/"
docker run --rm -v leobbs_boarddata:/data -v /tmp/leobbs_restore/boarddata:/backup alpine sh -c "rm -rf /data/* && cp -a /backup/. /data/"
docker run --rm -v leobbs_usr:/data -v /tmp/leobbs_restore/usr:/backup alpine sh -c "rm -rf /data/* && cp -a /backup/. /data/"

# 重新启动
docker compose up -d

# 清理临时文件
rm -rf /tmp/leobbs_restore
```

---

## 目录结构

```
leobbsx051108/
├── Dockerfile              # Docker 镜像构建文件
├── docker-compose.yml      # Docker Compose 编排文件
├── backup.sh               # 数据备份脚本
├── cgi-bin/                # CGI 程序目录（Perl 脚本）
│   ├── index.cgi           # 论坛首页
│   ├── install.cgi         # 安装程序
│   ├── admin.cgi           # 管理后台
│   ├── data/               # 论坛配置
│   ├── members/            # 用户数据
│   ├── messages/           # 帖子数据
│   └── boarddata/          # 版块数据
└── non-cgi/                # 静态资源目录
    ├── images/             # 图片资源
    ├── usr/                # 用户上传文件
    └── emot/               # 表情图片
```

---

## 自定义端口

修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "你的端口:80"
```

---

## 注意事项

- 本论坛程序发布于 2005 年，仅供学习研究和怀旧使用
- 程序编码为 GBK/GB2312，浏览器需要支持中文编码
- 首次启动后请尽快完成安装并设置管理员密码
- 建议定期执行备份脚本保存论坛数据

---

## 技术栈

- **程序语言**：Perl 5 (CGI)
- **Web 服务器**：Apache 2.4 (mod_cgi)
- **操作系统**：Debian Bullseye (Docker)
- **数据存储**：文件系统（无需数据库）
