#!/bin/bash
#
# LeoBBS X 数据备份脚本
# 备份论坛所有持久化数据（用户、帖子、配置等）
#

set -e

# 备份目标目录（可通过参数指定）
BACKUP_DIR="${1:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="leobbs_backup_${TIMESTAMP}"
CONTAINER_NAME="leobbs-forum"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}===========================================${NC}"
echo -e "${GREEN}  LeoBBS X 数据备份工具${NC}"
echo -e "${GREEN}===========================================${NC}"
echo ""

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}错误: Docker 未运行，请先启动 Docker${NC}"
    exit 1
fi

# 检查容器是否存在
if ! docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo -e "${RED}错误: 容器 ${CONTAINER_NAME} 不存在，请先启动论坛${NC}"
    exit 1
fi

# 创建备份目录（使用绝对路径）
mkdir -p "${BACKUP_DIR}"
BACKUP_DIR="$(cd "${BACKUP_DIR}" && pwd)"
BACKUP_FILE="${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"

echo -e "${YELLOW}开始备份论坛数据...${NC}"
echo "备份时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 直接从运行中的容器内用 root 权限打包所有数据
echo "  备份论坛配置数据..."
echo "  备份用户数据..."
echo "  备份帖子/消息数据..."
echo "  备份版块数据..."
echo "  备份用户上传文件..."
echo ""
echo -n "打包压缩备份文件..."

docker exec "${CONTAINER_NAME}" tar -czf /tmp/leobbs_backup.tar.gz \
    -C / \
    var/www/html/cgi-bin/data \
    var/www/html/cgi-bin/members \
    var/www/html/cgi-bin/messages \
    var/www/html/cgi-bin/boarddata \
    var/www/html/cgi-bin/record \
    var/www/html/cgi-bin/sale \
    var/www/html/cgi-bin/ebankdata \
    var/www/html/cgi-bin/memblock \
    var/www/html/cgi-bin/memfav \
    var/www/html/cgi-bin/memfriend \
    var/www/html/cgi-bin/ftpdata \
    var/www/html/non-cgi/usr \
    var/www/html/non-cgi/usravatars

docker cp "${CONTAINER_NAME}":/tmp/leobbs_backup.tar.gz "${BACKUP_FILE}"
docker exec "${CONTAINER_NAME}" rm -f /tmp/leobbs_backup.tar.gz

echo -e " ${GREEN}✓${NC}"

# 显示备份结果
BACKUP_SIZE=$(du -sh "${BACKUP_FILE}" | cut -f1)
echo ""
echo -e "${GREEN}===========================================${NC}"
echo -e "${GREEN}  备份完成！${NC}"
echo -e "${GREEN}===========================================${NC}"
echo "  文件: ${BACKUP_FILE}"
echo "  大小: ${BACKUP_SIZE}"
echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 清理旧备份（保留最近 10 个）
BACKUP_COUNT=$(ls -1 "${BACKUP_DIR}"/leobbs_backup_*.tar.gz 2>/dev/null | wc -l)
if [ "${BACKUP_COUNT}" -gt 10 ]; then
    echo -e "${YELLOW}清理旧备份（保留最近 10 个）...${NC}"
    ls -1t "${BACKUP_DIR}"/leobbs_backup_*.tar.gz | tail -n +11 | xargs rm -f
    echo -e "  ${GREEN}✓ 已清理${NC}"
fi
