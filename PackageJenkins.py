#-*- coding=utf-8 -*-
import os
import json as simplejson
import hashlib
import sys
from xml.etree import ElementTree as ET
reload(sys)
sys.setdefaultencoding('utf-8')

svn_executable = "/opt/homebrew/bin/svn"  # Example absolute path to svn executable
svnCommand = "{} info {{}} -R --xml".format(svn_executable)  # 修改此處以適應絕對路徑的格式

def GetAllVersion(root):
    print("SvnInfo Path:", root)
    command = svnCommand.format(root)  # 這裡已經使用.format()方法插入目錄
    with os.popen(command) as readStream:
        try:
            svnInfo = ET.parse(readStream)
        except Exception as e:
            print("SVN Info Parse Fail: ", e)
            return dict()

    result = dict()
    for file in svnInfo.iter():
        if file.get("kind") == "file":
            path = file.get("path")
            version = file.find("commit").get("revision")
            result[path] = version
    return result

def CreateJsonData(item, folder, folderPath, svnTable):
    total_size = 0
    if svnTable is None:
        svnTable = GetAllVersion(folderPath)

    distList = os.listdir(folderPath)
    for fileName in distList:
        realPath = folderPath + fileName
        if folderPath != "./":
            realPath = folderPath + "/" + fileName
        if os.path.isdir(realPath):
            total_size += CreateJsonData(item, folder + "/" + fileName, realPath, svnTable)
        else:
            if ".lua" in fileName:
                total_size += os.path.getsize(realPath)
                fileName = fileName.replace(".lua", ".dat")
                SetJsonElement(item, folder + "/" + fileName, GetVersionWithTable(os.path.abspath(realPath), svnTable))
            elif fileName[-3:] != '.py' and fileName != 'Version.json' and not ('.DS_Store' in fileName) and not ('.svn' in fileName) and not ('.md' in fileName):
                total_size += os.path.getsize(realPath)
                SetJsonElement(item, folder + "/" + fileName, GetVersionWithTable(os.path.abspath(realPath), svnTable))
    return total_size

def CreateJsonFile(data, filename):
    try:
        jsondata = simplejson.dumps(data, indent=4, skipkeys=True, sort_keys=True)
        fd = open(filename, 'w')
        fd.write(jsondata)
        fd.close()
    except Exception as e:
        print('ERROR writing', filename, e)

def SetJsonElement(item, key, value):
    if isinstance(value, int):
        item[key] = value
    else:
        raise Exception("The data is not control reversion for svn: ", key)

def GetVersionWithTable(filename, svnTable):
    version = int(svnTable.get(filename, '-1'))  # 找不到回傳 -1
    if version == -1:
        return GetVersion(filename)
    else:
        return version

def GetVersion(filename):
    command = svnCommand.format(filename)
    rs = ''.join(l for l in os.popen(command).readlines())
    root = ET.fromstring(rs)
    for i in root.findall('entry'):
        if i.get("kind") == 'file':
            return int(i.find('commit').get("revision"))

def CreateJsonDataMD5(item, fileName, rootFolder):
    dataPath = os.path.normpath(fileName)
    n = dataPath[dataPath.index(rootFolder) + len(rootFolder) + 1:]
    n = n[n.index(os.sep) + 1:]
    n = "/" + n
    item[n] = GetMd5(item, fileName)

def GetMd5(item, fileName):
    m = hashlib.md5()
    try:
        fd = open(fileName, "rb")
    except IOError as e:
        print("Reading file has problem:", fileName, e)
        return
    x = fd.read()
    fd.close()
    m.update(x)
    return m.hexdigest()

if __name__ == "__main__":
    item = {}
    CreateJsonData(item, '', './', None)
    CreateJsonFile(item, "Version.json")
    print("Create Version.json complete!")