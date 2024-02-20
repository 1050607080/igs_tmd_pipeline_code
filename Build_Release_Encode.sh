MODE=$1
echo "Start Build_Release_Encode.sh in $MODE mode"

if [ "$MODE" == "debug" ]; then
    /Library/Frameworks/Python.framework/Versions/2.7/bin/python CreateDownloadResourceEncode.py -m debug -p mac -b false
    /Library/Frameworks/Python.framework/Versions/2.7/bin/python CreateAllVersionEncode.py -m debug
elif [ "$MODE" == "release" ]; then
    /Library/Frameworks/Python.framework/Versions/2.7/bin/python CreateDownloadResourceEncode.py -m release -p mac -b false
    /Library/Frameworks/Python.framework/Versions/2.7/bin/python CreateAllVersionEncode.py -m release
else
    echo "Unknown mode: $MODE"
    exit 1
fi