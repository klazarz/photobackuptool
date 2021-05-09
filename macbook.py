import osxphotos
import datetime
import os
import shutil

from datetime import date, timedelta
from exif import Image
from osxphotos.imageconverter import ImageConverter


def main():

    # This is yesterday's date - relevant for daily exports
    today = date.today()
    yesterday = today - timedelta(days = 1)
    tod_str = tod_str = datetime.datetime.strftime(today, '%Y%m%d')
    
    # yes_year = yesterday.strftime('%Y')
    # yes_month = yesterday.strftime('%m')
    # yes_day = yesterday.strftime('%d')

    # Start exporting photos from this date onwards
    
    if os.path.exists('last_run.txt'):
        with open('last_run.txt') as f:
            lines = f.readlines()
        
        # print(lines[-1].replace('-',''))
        lastrun_str=lines[-1].replace('-','').replace('\n','')
        yes_str = lines[-1].replace('-','').replace('\n','')

        if yes_str == tod_str:
            exit()

    else:
         yes_str = yesterday.strftime('%Y%m%d')

   
   
    # yes_str = '20210506'
    # tod_str = '20210507'

    photosdb = osxphotos.PhotosDB()
    # photos = photosdb.photos(from_date=datetime.datetime.strptime(yes_str, '%Y%m%d'))
    photos = photosdb.photos()

    i=0

    for p in photos:
        added = datetime.datetime.strftime(p.date_added, '%Y%m%d')
        if added >= lastrun_str and added < tod_str and not p.shared or p.shared == None:
            # print(added)
            if hasattr(p.exif_info, 'camera_model'):
                fold_struc = "/Users/kevin/Desktop/photobackup/%Y/%m/" + str(p.exif_info.camera_model)
            else:
                fold_struc='/Users/kevin/Desktop/photobackup/%Y/%m/none/'

            fold_struc_mov = '/Users/kevin/Desktop/photobackup/%Y/%m/movies/'

            os.makedirs(p.date.strftime(fold_struc_mov), exist_ok=True)
            os.makedirs(p.date.strftime(fold_struc), exist_ok=True)

            mov_dir = p.date.strftime(fold_struc_mov)
            photo_dir = p.date.strftime(fold_struc)

            new_name = p.date.strftime('%Y%m%d') + '_' + p.original_filename

            if p.ismovie:
                p.export(mov_dir, p.date.strftime('%Y%m%d') + '_' + p.original_filename)
            else:
                if p.hasadjustments:
                    p.export(p.date.strftime(fold_struc), p.date.strftime('%Y%m%d') + '_' + p.original_filename, edited=True, use_photos_export=True)
                else:
                    p.export(p.date.strftime(fold_struc), p.date.strftime('%Y%m%d') + '_' + p.original_filename, use_photos_export=True)
            
            conversion(photo_dir)
            
        i += 1



    os.system('echo ' + str(today) + ': ' + str(i) + ' files. >> log.txt')
    os.system('echo ' +str(today) + '>> last_run.txt')
    



def conversion(photo_dir):
    basepath = photo_dir
    with os.scandir(basepath) as entries:
        for entry in entries:
            photofile = entry.name
            if entry.name.lower().endswith('.heic'):      
                base = os.path.splitext(photofile)[0]
                new_name_jpg = str(base + '.jpg')
                converter = ImageConverter()
                input = photo_dir + '/' + photofile
                output = photo_dir + '/' + str(new_name_jpg)
                converter.write_jpeg(input, output)
                os.remove(input)
               

if __name__ == "__main__":
    main()
