#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import sys
import re
from xml.etree import ElementTree as ET
import os
import shutil
import json

# 确保有足够的命令行参数
if len(sys.argv) < 2:
    sys.exit(1)

platform = sys.argv[1]  # 接受的第一个命令行参数：平台

FILE_NAME = "/Users/tmd/Documents/tmd/SouthPark/Jenkins/SyncFileTemp/Temp/update.ffs_batch" 
FILE_BAT = "/Users/tmd/Documents/tmd/SouthPark/Jenkins/SyncFileTemp/Temp/update.bat"

OUTPUT_NAME = "/Users/tmd/Documents/tmd/SouthPark/Jenkins/SyncFileTemp/Output/{0}/update.ffs_batch"
OUTPUT_BAT = "/Users/tmd/Documents/tmd/SouthPark/Jenkins/SyncFileTemp/Output/{0}/update.bat"

OUTPUT_DIR = "/Users/tmd/Documents/tmd/SouthPark/Jenkins/SyncFileTemp/Output/{0}" # 輸出資料夾

PROJECT_XML = "/Users/tmd/Documents/tmd/SouthPark/ClientCocos/proj.android/gameName.xml"         # 遊戲列表
VERSION_FILE = "/Users/tmd/Documents/tmd/SouthPark/ClientCocos/proj.android/targetVersion.json"  # 三平台版本


# 版本列表
ANDROID = "Android"
IOS = "iOS"

# 平台資料夾
INANNA = "Inanna"

# 三平台版本
with open(VERSION_FILE) as version_file:
    jdata = json.load(version_file, encoding = "utf8")

# 版本數量
def get_version_count(gameName,platform):
    versionCount = 0
    if platform == ANDROID or platform == IOS:
        if gameName != INANNA:
            versionCount += 2
        for platform in jdata:
            for v in jdata[platform]:
                if gameName == INANNA and platform == platform:
                    versionCount += 1
                elif gameName != INANNA:
                    versionCount += 1
    else:
        versionCount = 1
    return versionCount


# 讀取資料夾名稱
try:
    tree = ET.ElementTree( file = PROJECT_XML)
except ET.ParseError:
    print("Parse XML error : " + PROJECT_XML)

# 讀入檔案
b = open(FILE_BAT, "r")
file_bat_list = b.read()
b.close()

# 輸出檔案
for elem in tree.iterfind("game[@name]"):
    targetDir = elem[2].text
    versionLower = str(platform).lower()

    # 刪除原本的資料夾
    if os.path.isdir(OUTPUT_DIR.format(targetDir)):
        shutil.rmtree(OUTPUT_DIR.format(targetDir))

    os.mkdir(OUTPUT_DIR.format(targetDir))

    # bat 檔案
    output = open(OUTPUT_BAT.format(targetDir), "w+")
    file_bat_list_new = re.sub(r"<Path>", r"/w D:\\TMD_PUBLIC\\TMD\\testing\\{0}\\{1}\\update.ffs_batch".format(versionLower, targetDir), file_bat_list, 1)
    output.write(file_bat_list_new)
    output.close()

    # FileSync 檔案
    # 先產出與版本數量一致的<Pair></Pair>
    copy_list = []
    with open(FILE_NAME.format(targetDir), "r") as fn:
        with open(OUTPUT_NAME.format(targetDir), "w") as on:
            for line in fn:
                if "<Pair>" in line or "<Left/>" in line or "<Right/>" in line:
                    copy_list.append(line)
                elif "</Pair>" in line:
                    copy_list.append(line)
                    for index in range(get_version_count(targetDir,platform)):
                        for copy in copy_list:
                            on.write(copy)
                else:
                    on.write(line)
    # 再將<Left>和<Right>的路徑以替換字串的方式寫入
    r = open(OUTPUT_NAME.format(targetDir), "r")
    file_list = r.read()
    r.close()
    w = open(OUTPUT_NAME.format(targetDir), "w+")
    w.truncate(0)
    if platform == ANDROID or platform == IOS:
        # android同步ios
        if targetDir != INANNA:
            file_list = re.sub(r"<Left/>", r"<Left>D:\\TMD_PUBLIC\\TMD\\testing\\android\\{0}</Left>".format(targetDir), file_list, 1)
            file_list = re.sub(r"<Right/>", r"<Right>D:\\TMD_PUBLIC\\TMD\\testing\\ios\\{0}</Right>".format(targetDir), file_list, 1)
            file_list = re.sub(r"<Left/>", r"<Left>D:\\TMD_PUBLIC\\TMD\\testing\\android\\{0}</Left>".format(targetDir), file_list, 1)
            file_list = re.sub(r"<Right/>", r"<Right>D:\\TMD_PUBLIC\\TMD\\testing\\win\\{0}</Right>".format(targetDir), file_list, 1)
        # 同步二測
        for platform in jdata:
            for version in jdata[platform]:
                if targetDir != INANNA:
                    file_list = re.sub(r"<Left/>", r"<Left>D:\\TMD_PUBLIC\\TMD\\testing\\android\\{0}</Left>".format(targetDir), file_list, 1)
                    file_list = re.sub(r"<Right/>", r"<Right>\\\\10.100.40.55\\webgame\\Game\\TMD_mobile_test\\data\\{0}\\{1}</Right>".format(version, targetDir), file_list, 1)
                elif targetDir == INANNA and platform == platform:
                    file_list = re.sub(r"<Left/>", r"<Left>D:\\TMD_PUBLIC\\TMD\\testing\\{0}\\{1}</Left>".format(versionLower, targetDir), file_list, 1)
                    file_list = re.sub(r"<Right/>", r"<Right>\\\\10.100.40.55\\webgame\\Game\\TMD_mobile_test\\data\\{0}\\{1}</Right>".format(version, targetDir), file_list, 1)
    else:
        file_list = re.sub(r"<Left/>", r"<Left>D:\\TMD_PUBLIC\\TMD\\testing\\{0}\\{1}</Left>".format(versionLower, targetDir), file_list, 1)
        file_list = re.sub(r"<Right/>", r"<Right>\\\\10.100.40.55\\webgame\\Game\\TMD_mobile_test\\data\\{0}\\{1}</Right>".format(versionLower, targetDir), file_list, 1)
    w.write(file_list)
    w.close()

print("replace_jenkins end")