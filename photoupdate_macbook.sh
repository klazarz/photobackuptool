#!/bin/bash
#PATH=/Users/kevin/anaconda/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Applications/Server.app/Contents/ServerRoot/usr/bin:/Applications/Server.app/Contents/ServerRoot/usr/sbin:/Library/Frameworks/Mono.framework/Versions/Current/Commands:/Users/kevin/Documents/python_projects/photobackuptool

python3.9 /Users/kevin/Documents/photobackuptool/macbook.py

rsync -rtuv /Users/kevin/Desktop/photobackup/* kevin@192.168.1.200:/Volumes/YOGI/photos/.

rm -rf /Users/kevin/Desktop/photobackup/*


