# photobackuptool
Script to create a backup that contains all photos from previous day in Apple Photo app

## Added a cronjob:
The cronjob runs on the mac mini every night at 00:01 to create a daily backup of photos taken on the previous day.
```1 00 * * * /bin/zsh /Users/kevin/Documents/python_projects/photobackuptool/photoupdate.sh```

