#! /bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

/Library/Frameworks/Python.framework/Versions/2.7/bin/python ${DIR}/build_native_jenkins.py -b release

'''chmod +x /Users/tmd/Documents/tmd/SouthPark/ClientCocos/proj.android-studio/gradlew
/Users/tmd/Documents/tmd/SouthPark/ClientCocos/proj.android-studio/gradlew assembleRelease'''