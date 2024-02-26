#!/bin/sh

# 定義源目錄和目標目錄
SOURCE_DIR="/Users/tmd/Documents/tmd/SouthPark/ClientCocos/bin/release/tmp"
TARGET_DIR="/Users/tmd/Documents/tmd/SouthPark/ClientCocos/proj.android/assets"

# 清空目標目錄下的所有文件（謹慎使用，確保路徑正確！）
rm -rf ${TARGET_DIR}/*

# 從源目錄復制文件到目標目錄
cp -R ${SOURCE_DIR}/* ${TARGET_DIR}

# 在目標目錄執行SVN更新操作
svn update ${TARGET_DIR}

echo "move_and_update_assets 完成成功。"