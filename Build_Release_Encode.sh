#!/bin/bash
MODE=$1  # 获取第一个命令行参数
echo "Start Build_Release_Encode.sh in $MODE mode"

if [ "$MODE" == "debug" ]; then
    /Library/Frameworks/Python.framework/Versions/2.7/bin/python CreateDownloadResourceEncode.py -m debug -p ios -b false
    /Library/Frameworks/Python.framework/Versions/2.7/bin/python CreateAllVersionEncode.py -m debug
elif [ "$MODE" == "release" ]; then
    /Library/Frameworks/Python.framework/Versions/2.7/bin/python CreateDownloadResourceEncode.py -m release -p ios -b false
    /Library/Frameworks/Python.framework/Versions/2.7/bin/python CreateAllVersionEncode.py -m release
else
    echo "Unknown mode: $MODE"
    exit 1
fi

# 由于Jenkins构建通常不是交互式的，建议移除下面这行
# read -p "Press [Enter] key to continue..."