#!/bin/bash
echo "Start Build_Release_Encode.sh"
python CreateDownloadResourceDecode.py -m release -p win -b false
python CreateAllVersionDecode.py -m release
read -p "Press [Enter] key to continue..."