#!/bin/bash
echo "Start Build_Release_Encode.sh"
python CreateDownloadResourceEncode.py -m release -p win -b false
python CreateAllVersionEncode.py -m release
read -p "Press [Enter] key to continue..."