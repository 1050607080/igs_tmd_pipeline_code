import os
import json
import argparse
import PackageJenkins

CONFIG_FILE = "build-cfg-original.json"
VERSION_FILE = "AllVersion.json"

INANNA_DEFINE_LUA_PATTERN = "Define.lua"
DEFINE_LUA_PATTERN = "_Define.lua"

parser = argparse.ArgumentParser( description = 'create download resource arg parser' )
parser.add_argument( "-m", "--mode", type=str, choices=["debug","release"], default="debug" )

args = parser.parse_args()

print( "use mode: " + args.mode )

if args.mode == "debug":
    folder = "../bin/debug/"
else:
    folder = "../bin/release/"

def createAllVersionFile( rootPath ):
    path = os.path.join( rootPath, CONFIG_FILE )
    try:
        f = open(path)
        cfg = json.load(f, encoding='utf8')
        f.close()
    except Exception:
        print("Configuration file \"%s\" is not existed or broken!" % path)
    resources       = cfg["copy_resources"]
    
    rootFolder          = os.path.join( rootPath, folder )
    tmpFolder           = os.path.join( rootPath, folder + "tmp/InannaLua" )
    tmpPath             = os.path.normpath( tmpFolder )
    versionJsonPath     = os.path.join( tmpPath, VERSION_FILE )

    allversion = {}
    for res in resources:
        original = os.path.join( rootPath, res['from'] )
        for dirpath, dirnames, filenames in os.walk( original ):
            found = False
            for filename in filenames:
                if DEFINE_LUA_PATTERN in filename:
                    defineFilePath = os.path.normpath( os.path.join( dirpath, filename ) )
                    tokens = filename.split( DEFINE_LUA_PATTERN )
                    print( filename + " : " , PackageJenkins.GetVersion( defineFilePath ) )
                    allversion[tokens[0]] = PackageJenkins.GetVersion( defineFilePath )
                    found = True
                    break
                if INANNA_DEFINE_LUA_PATTERN == filename:
                    defineFilePath = os.path.normpath( os.path.join( dirpath, filename ) )
                    print( filename + " : " , PackageJenkins.GetVersion( defineFilePath ) )
                    allversion["Inanna"] = PackageJenkins.GetVersion( defineFilePath )
                    found = True 
            if found:
                break
    PackageJenkins.CreateJsonFile( allversion, versionJsonPath )

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
    createAllVersionFile( current_dir )