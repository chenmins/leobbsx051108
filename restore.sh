#!/bin/bash
#
# LeoBBS X 数据恢复脚本
# 从备份文件恢复论坛所有数据
#

set -e

CONTAINER_NAME="leobbs-forum"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}===========================================${NC}"
echo -e "${GREEN}  LeoBBS X 数据恢复工具${NC}"
echo -e "${GREEN}===========================================${NC}"
echo ""

# 检查参数
if [ -z "$1" ]; then
    echo -e "${RED}用法: ./restore.sh <备份文件路径>${NC}"
    echo ""
    echo "示例:"
    echo "  ./restore.sh ./backups/leobbs_backup_20260609_173213.tar.gz"
    echo ""
    # 列出可用备份
    if ls ./backups/leobbs_backup_*.tar.gz > /dev/null 2>&1; then
        echo "可用的备份文件:"
        ls -1t ./backups/leobbs_backup_*.tar.gz | while read f; do
            echo "  $f  ($(du -sh "$f" | cut -f1))"
        done
    fi
    exit 1
fi

BACKUP_FILE="$1"

# 检查备份文件是否存在
if [ ! -f "${BACKUP_FILE}" ]; then
    echo -e "${RED}错误: 备份文件不存在: ${BACKUP_FILE}${NC}"
    exit 1
fi

# 转为绝对路径
BACKUP_FILE="$(cd "$(dirname "${BACKUP_FILE}")" && pwd)/$(basename "${BACKUP_FILE}")"

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}错误: Docker 未运行，请先启动 Docker${NC}"
    exit 1
fi

# 检查容器是否存在
if ! docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo -e "${RED}错误: 容器 ${CONTAINER_NAME} 不存在，请先执行 docker compose up -d${NC}"
    exit 1
fi

# 确认恢复操作
echo -e "${YELLOW}警告: 恢复操作将覆盖当前论坛的所有数据！${NC}"
echo ""
echo "  备份文件: ${BACKUP_FILE}"
echo "  文件大小: $(du -sh "${BACKUP_FILE}" | cut -f1)"
echo ""
read -p "确认要恢复吗？(输入 yes 继续): " CONFIRM

if [ "${CONFIRM}" != "yes" ]; then
    echo ""
    echo "已取消恢复操作。"
    exit 0
fi

echo ""
echo -e "${YELLOW}开始恢复论坛数据...${NC}"
echo "恢复时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 将备份文件拷贝到容器内并解压恢复
echo -n "  上传备份文件到容器..."
docker cp "${BACKUP_FILE}" "${CONTAINER_NAME}":/tmp/leobbs_restore.tar.gz
echo -e " ${GREEN}✓${NC}"

echo -n "  解压并恢复数据..."
docker exec "${CONTAINER_NAME}" sh -c "cd / && tar -xzf /tmp/leobbs_restore.tar.gz"
echo -e " ${GREEN}✓${NC}"

echo -n "  修复文件权限..."
docker exec "${CONTAINER_NAME}" sh -c "\
    chown -R www-data:www-data /var/www/html/cgi-bin/data && \
    chown -R www-data:www-data /var/www/html/cgi-bin/members && \
    chown -R www-data:www-data /var/www/html/cgi-bin/messages && \
    chown -R www-data:www-data /var/www/html/cgi-bin/boarddata && \
    chown -R www-data:www-data /var/www/html/cgi-bin/record && \
    chown -R www-data:www-data /var/www/html/cgi-bin/sale && \
    chown -R www-data:www-data /var/www/html/cgi-bin/ebankdata && \
    chown -R www-data:www-data /var/www/html/cgi-bin/memblock && \
    chown -R www-data:www-data /var/www/html/cgi-bin/memfav && \
    chown -R www-data:www-data /var/www/html/cgi-bin/memfriend && \
    chown -R www-data:www-data /var/www/html/cgi-bin/ftpdata && \
    chown -R www-data:www-data /var/www/html/non-cgi/usr && \
    chown -R www-data:www-data /var/www/html/non-cgi/usravatars"
echo -e " ${GREEN}✓${NC}"

echo -n "  清理临时文件..."
docker exec "${CONTAINER_NAME}" rm -f /tmp/leobbs_restore.tar.gz
echo -e " ${GREEN}✓${NC}"

echo ""
echo -e "${GREEN}===========================================${NC}"
echo -e "${GREEN}  恢复完成！${NC}"
echo -e "${GREEN}===========================================${NC}"
echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "论坛已恢复，请访问 http://localhost:8080/cgi-bin/leobbs.cgi 确认。"
