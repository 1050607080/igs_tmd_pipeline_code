# -*- encoding:utf-8 -*-
import os
import shutil
import json
import zipfile
import subprocess
import argparse
import ntpath
import codecs
import platform
import Package
import glob
import time
from datetime import datetime
from distutils.dir_util import copy_tree

PACKAGE_CONFIG_FILE = "build-cfg-copyAssets.json"

CONFIG_FILE = "build-cfg-original.json"
CONFIG_FILE_IOS = "build-cfg-original-ios.json"
CONFIG_FILE_WIN = "build-cfg-original-win.json"

ANDROID_MANIFEST = "AndroidManifest.xml"
ENCRYPT_KEY = "SouthPark_oldrd2rg4"
SIGNATURE = "InternationalGameSystem"
FILE_TOTAL_SIZE = "totalSize"

parser = argparse.ArgumentParser( description = 'create download resource arg parser' )
parser.add_argument( "-m", "--mode", type=str, choices=["debug","release"], default="debug" )
parser.add_argument( "-p", "--platform", type=str, choices=["win","mac"], default="win" )
parser.add_argument( "-b", "--byteCode", type=str, choices=["true","false"], default="false" )
parser.add_argument( "-t", "--targetOS", type=str, choices=["android","ios", "win"], default="android" )

args = parser.parse_args()
currentOS = args.targetOS

print( "use mode: " + args.mode )
print( "platform: " + args.platform )
print( "byteCode: " + args.byteCode )
print( "targetOS: " + currentOS )

if args.mode == "debug":
    folder = "../bin/debug/"
else:
    folder = "../bin/release/"

times = datetime(year=2017,month=5,day=31,hour=9)
timeSecond = time.mktime(times.timetuple())

def SetWriteTime( path ):
    os.utime(path, (timeSecond, timeSecond))

# 合圖壓縮
def custom_pngquant( app_android_root ):
    configFile = CONFIG_FILE
    if currentOS == "ios":
        configFile = CONFIG_FILE_IOS
    elif currentOS == "win":
        configFile = CONFIG_FILE_WIN
    
    print( "custom_pngquant configFile: " + configFile )
    path = os.path.join(app_android_root, configFile)
    try:
        f = open(path)
        cfg = json.load(f, encoding='utf8')
        f.close()
    except Exception:
        print("Configuration file \"%s\" is not existed or broken!" % path)
    resources = cfg["copy_resources"]

    path = os.path.normpath(os.path.join(app_android_root, PACKAGE_CONFIG_FILE))
    try:
        f = open(path)
        cfg = json.load(f, encoding='utf8')
        f.close()
    except Exception:
        print("Configuration file \"%s\" is not existed or broken!" % path)
    pngList = cfg["png_needCompress"]
    # for res in pngList:
    #     print("KK", res)

    for res in resources:
        original = os.path.join( app_android_root, res['from'] )
        if res['to'] not in ["cocos"] and res['zip']:
            for dirpath, dirnames, filenames in os.walk(original):
                for filename in filenames:
                    for res in pngList:
                        if res in filename:
                            # print( "custom_pngquant", filename, dirpath )
                            os.system(".\\pngquant\\pngquant --ext=.png --force " + dirpath + "\\" + filename )
                            # os.system(".\\pngquant\\pngquant --force " + dirpath + "\\" + filename )


def check_BOM_UTF8( fileName ):
    filehandle = open(fileName,'r')
    content = filehandle.read()
    filehandle.close()
    if content[:3] == codecs.BOM_UTF8:
        raise Exception("codecs.BOM_UTF8 :", fileName)

def copy_resources( app_android_root ):
    configFile = CONFIG_FILE
    if currentOS == "ios":
        configFile = CONFIG_FILE_IOS
    elif currentOS == "win":
        configFile = CONFIG_FILE_WIN
    
    print( "copy_resources configFile: " + configFile )
    path = os.path.join(app_android_root, configFile)
    try:
        f = open(path)
        cfg = json.load(f, encoding='utf8')
        f.close()
    except Exception:
        print("Configuration file \"%s\" is not existed or broken!" % path)
    resources       = cfg["copy_resources"]
    
    rootFolder   = os.path.join( app_android_root, folder )
    tmpFolder    = os.path.join( app_android_root, folder + "tmp/" )
    tmpPath      = os.path.normpath( tmpFolder )

    #resourceZIP  = os.path.join(app_android_root, folder + "CopyToServer.zip")
    # print( "rootFolder: " + rootFolder )
    # print( "tmpFolder: " + tmpFolder )
    # print( "tmpPath: " + tmpPath )

    if os.path.isdir( tmpFolder ):
        shutil.rmtree( tmpFolder )
    #if os.path.exists(resourceZIP):
    #    os.remove(resourceZIP)
    
    # copy file to folder tmp
    for res in resources:
        print("Start package resource: " + res['to'])
        original    = os.path.join( app_android_root, res['from'] )
        toPath      = os.path.join( tmpFolder, res['to'] )
        jsonPath    = os.path.join( toPath, "Version.json" )
        zipFileName     = os.path.join( toPath, ntpath.basename( toPath ) + ".zip" )
        
        #升級svn版本
        if "root" in res.keys():
            print("value!! : "+ res['root'] )
            cmdStr="svn upgrade ../../../"+ res['root']
            subprocess.call( cmdStr, shell=True )

        totalSize = 0
        #check lua utf-8 wirh BOM
        if not res['zip']:
            for dirpath, dirnames, filenames in os.walk(original):
                for filename in filenames:
                    directFilePath = os.path.normpath(os.path.join(dirpath,filename))
                    check_BOM_UTF8(directFilePath)

        #忽略svn檔案
        patterns = set(
            [
                ".svn",
                "WebEnvironment.xml",
                "*.md"
            ]
        )
        shutil.copytree( original, toPath, ignore = shutil.ignore_patterns(*patterns) )


        #執行圖檔加密
        # if "Resource" in toPath and currentOS == 'win':
            # subprocess.call(['python', 'pngencrypt.py', toPath])
        # print("pngencrypt end", toPath)

        if res['zip']:
            # package zip
            f = zipfile.ZipFile( zipFileName, 'w', zipfile.ZIP_DEFLATED ) 
            for dirpath, dirnames, filenames in os.walk( toPath ):
                #print( "dirpath: " + dirpath )
                for filename in filenames: 
                    if '.zip' in filename:
                        continue
                    elif 'Version.json' in filename:
                        continue
                    elif 'LocalVersion.json' in filename:
                        continue
                    else:
                        dataPath = os.path.normpath( os.path.join( dirpath, filename ) )
                        n = dataPath[dataPath.index( tmpPath ) + len( tmpPath )+1:]
                        n = n[n.index(os.sep)+1:]                
                        f.write( dataPath, n )
            f.close()

            # create json file
            item = {}

            item[FILE_TOTAL_SIZE] = os.path.getsize( os.path.normpath( zipFileName ) )

            print( "tmpPath: " + tmpPath )
            print( "zipFileName: " + os.path.normpath( zipFileName ) )
            Package.CreateJsonDataMD5( item, os.path.normpath( zipFileName ), tmpPath )
            Package.CreateJsonFile( item, jsonPath )
            Package.CreateJsonFile( item, os.path.join( toPath, "LocalVersion.json" ) )
        else:
            item = {}
            print("Create version json file: " + jsonPath)
            totalSize = Package.CreateJsonData( item, '', original, None )
            #print("Save totalSize : " , totalSize )

            print("Save version file to : " + jsonPath )
            Package.CreateJsonFile( item, jsonPath )
            Package.CreateJsonFile( item, os.path.join( toPath, "LocalVersion.json" ) )
            print(" ------------------ ")

def package_Split(app_android_root):
    path = os.path.normpath(os.path.join(app_android_root, PACKAGE_CONFIG_FILE))
    try:
        f = open(path)
        cfg = json.load(f, encoding='utf8')
        f.close()
    except Exception:
        print("Configuration file \"%s\" is not existed or broken!" % path)
    resources       = cfg["copy_resources"]

    rootFolder   = os.path.join( app_android_root, folder )
    tmpFolder    = os.path.join( app_android_root, folder + "tmp/" )
    tmpPath      = os.path.normpath( tmpFolder )

    #remove all zip file
    for res in resources:
        if "ZipPath" in res:
            tmpZipPath = os.path.normpath( tmpPath + "/" + res["ZipPath"] )
            distList = os.listdir(tmpZipPath)
            for fileName in distList:
                if ".zip" in fileName:                    
                    fileName = os.path.normpath( tmpZipPath + "/" + fileName )
                    os.remove( fileName )
        
    zipFileList = {};
    for res in resources:
        if "ZipPath" in res:
            tmpZipPath = os.path.normpath( tmpPath + "/" + res["ZipPath"] )
        if "ZipFile" in res:
            zipFileName,extension = os.path.splitext(res["ZipFile"])
            ZipFilePath = os.path.normpath( os.path.join( tmpZipPath, zipFileName ) )
            #print("Copy resource ZipFilePath: " + ZipFilePath )
            
            for data in res['DataSrc']:
                dir_src    = os.path.normpath( tmpPath + "/" + data['from'] )
                #print(" dir_src: " + dir_src )
                toPath = os.path.normpath(os.path.join(ZipFilePath, data['to']))
                #print(" toPath: " + toPath )
                src_files = glob.glob( dir_src )
 
                if not os.path.isdir( toPath ):
                    os.makedirs( toPath )
                if os.path.isfile( dir_src ) or os.path.isdir( dir_src ):
                
                    for item in src_files:
                        for path,dirname,files in os.walk( toPath ):
                            try:
                               if toPath == path:
                                 # 複製文件
                                 shutil.copy( item, path )                                 
                                 #print("Copy resource copy src: " + item )
                                 #print("Copy resource copy path: " + path )
                            except:
                                #print("Copy resource copy_tree src: " + item )
                                #print("Copy resource copy_tree path: " + path )
                                # 複製資料夾
                                copy_tree( dir_src, path )

            if "exclude" in res:
                #remove not used folder or file
                for item in res["exclude"]:
                    excludeFileOrFolder = os.path.normpath(os.path.join(toPath,item))
                    if os.path.isfile(excludeFileOrFolder):
                        os.remove(excludeFileOrFolder)
                    if os.path.isdir(excludeFileOrFolder):
                        shutil.rmtree(excludeFileOrFolder)

            if not zipFileList.has_key( tmpZipPath ):
                tmpZipFilePathList = [ ZipFilePath ]                        
                zipFileList[tmpZipPath] = tmpZipFilePathList
            else:
                tmpZipFilePathList = zipFileList[tmpZipPath]
                if tmpZipFilePathList.count( ZipFilePath ) == 0:
                    tmpZipFilePathList.append( ZipFilePath )


    '''
        Modified by WinthropChang at 2015/10/20
        
        Start to encrypt lua file
        Because we use Cocos2dx 3.2.This version doesn't support luajit 64bit.
        If we compile lua code to bytecode will crashed in iOS 64bit device.
        For security and void this issue we just encypt file not compile it.
        
        We can use our encrypt algorithm and decrypt in c++.
        Bu cocos provide a lua tool to do this(XXTEA).
        The algorithm is very simple.
        
        If you are interesting on it,please surf the wiki.
        
        https://en.wikipedia.org/wiki/XXTEA
    '''                    

    #pack resource to zip file
    for zipPath, zipFileList in zipFileList.items():
        totalSize = 0
        md5Value = {}
        for zipF in zipFileList:
            moduleZip = zipF + ".zip"
            #print("Zip resource C: " + moduleZip + " zipPath " + zipPath)
            if isWindows():
                if args.mode != "debug":
                    #注意空格是區分參數
                    os.system( "Powershell.exe -executionpolicy remotesigned -File .\SetTimeStamp\SetTimeStamp.ps1 "+zipF+ " \"5/31/2017 9:00 am\"" )
            f = zipfile.ZipFile(moduleZip,'w',zipfile.ZIP_DEFLATED) 
            for dirpath, dirnames, filenames in os.walk(zipF):
                if not isWindows():
                    os.system("touch -t 201705310900 " + dirpath )
                for filename in filenames: 
                    if ".wav" not in filename and ".DS_Store" not in filename:
                        dataPath = os.path.normpath( os.path.join(dirpath, filename) )
                        #強制修改檔案修改時間，避免MD5碼產生時不同
                        if not isWindows():
                            if args.mode != "debug":
                                SetWriteTime(dataPath)
                        else:
                            SetWriteTime(dataPath)
                        #print( "dataPath: " + dataPath )
                        n = dataPath[dataPath.index(zipPath)+len(zipPath)+1:]
                        n = n[n.index(os.sep)+1:]                 
                        #print( "n :", n )
                        f.write(dataPath,n)
            f.close()
                
            f = zipfile.ZipFile(moduleZip,'a',zipfile.ZIP_DEFLATED) 
            f.close()
        
            shutil.rmtree(zipF)
            ZipSize = os.path.getsize( moduleZip )
            totalSize = totalSize + ZipSize
        
            Package.CreateJsonDataMD5( md5Value, os.path.normpath( moduleZip ), tmpPath )
        
        md5Value[FILE_TOTAL_SIZE] = totalSize
        jsonFile      = os.path.normpath(os.path.join(zipPath,"Version.json"))
        localJSONFile = os.path.normpath(os.path.join(zipPath,"LocalVersion.json"))
        Package.CreateJsonFile( md5Value, jsonFile )
        Package.CreateJsonFile( md5Value, localJSONFile )

def isWindows():
    return platform.system() == "Windows"

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
    custom_pngquant( current_dir )
    copy_resources( current_dir )
    package_Split( current_dir )