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
TEMP_DIR="/tmp/${BACKUP_NAME}"
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

# 创建备份目录
mkdir -p "${BACKUP_DIR}"
mkdir -p "${TEMP_DIR}"

echo -e "${YELLOW}开始备份论坛数据...${NC}"
echo "备份时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 获取 docker-compose 项目名称前缀
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_NAME="$(basename "${PROJECT_DIR}" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g')"

# 备份各个 Volume
backup_volume() {
    local volume_suffix=$1
    local backup_subdir=$2
    local description=$3

    # 尝试多种 volume 命名格式
    local volume_name=""
    for prefix in "${PROJECT_NAME}" "leobbsx051108"; do
        if docker volume inspect "${prefix}_${volume_suffix}" > /dev/null 2>&1; then
            volume_name="${prefix}_${volume_suffix}"
            break
        fi
    done

    if [ -z "$volume_name" ]; then
        # 尝试直接使用 volume_suffix
        if docker volume inspect "${volume_suffix}" > /dev/null 2>&1; then
            volume_name="${volume_suffix}"
        else
            echo -e "  ${YELLOW}⚠ 跳过 ${description}（Volume 未找到）${NC}"
            return
        fi
    fi

    echo -n "  备份 ${description}..."
    docker run --rm \
        -v "${volume_name}":/source:ro \
        -v "${TEMP_DIR}":/backup \
        alpine sh -c "cp -a /source /backup/${backup_subdir}"
    echo -e " ${GREEN}✓${NC}"
}

backup_volume "leobbs_data" "data" "论坛配置数据"
backup_volume "leobbs_members" "members" "用户数据"
backup_volume "leobbs_messages" "messages" "帖子/消息数据"
backup_volume "leobbs_boarddata" "boarddata" "版块数据"
backup_volume "leobbs_usr" "usr" "用户上传文件"

# 打包压缩
echo ""
echo -n "打包压缩备份文件..."
BACKUP_FILE="${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
tar -czf "${BACKUP_FILE}" -C "${TEMP_DIR}" .
echo -e " ${GREEN}✓${NC}"

# 清理临时文件
rm -rf "${TEMP_DIR}"

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
