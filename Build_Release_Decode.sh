#!/bin/bash
echo "Start Build_Release_Encode.sh"
/Library/Frameworks/Python.framework/Versions/2.7/bin/python CreateDownloadResourceDecode.py -m release -p mac -b false
/Library/Frameworks/Python.framework/Versions/2.7/bin/python CreateAllVersionDecode.py -m release
read -p "Press [Enter] key to continue..."