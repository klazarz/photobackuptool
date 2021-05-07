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
    yes_str = yesterday.strftime('%Y%m%d')
    yes_year = yesterday.strftime('%Y')
    yes_month = yesterday.strftime('%m')
    yes_day = yesterday.strftime('%d')

    # Start exporting photos from this date onwards
    yes_str = '20210501'

    photosdb = osxphotos.PhotosDB()
    photos = photosdb.photos(from_date=datetime.datetime.strptime(yes_str, '%Y%m%d'))

    i=0

    for p in photos:
        # print(p.original_filename, 'shared: ', p.shared)
        if not p.shared or p.shared == None:
        # The folder structure - right now it is root / year / month
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
            # print('external edit: ', p.external_edit)

            # print('start processing: ', new_name)

            if p.ismovie:
                p.export(mov_dir, p.date.strftime('%Y%m%d') + '_' + p.original_filename)
            else:
                if p.hasadjustments:
                    p.export(p.date.strftime(fold_struc), p.date.strftime('%Y%m%d') + '_' + p.original_filename, edited=True, use_photos_export=True)
                else:
                    p.export(p.date.strftime(fold_struc), p.date.strftime('%Y%m%d') + '_' + p.original_filename, use_photos_export=True)
            
            # print('exported ', new_name, ' to ', fold_struc)

            # if p.ismovie:
            #     p.export(mov_dir, new_name)
            # else:
            #     if p.hasadjustments:
            #         p.export(photo_dir, new_name, edited=True, use_photos_export=True)
            #     else:
            #         p.export(photo_dir, new_name, use_photos_export=True)

            conversion(photo_dir)
            
            
            # print('after heic png check: ', new_name)
            
            # if not p.ismovie and not new_name.lower().endswith('.png'):
            #     basepath = prep_dir
            #     with os.scandir(basepath) as entries:
            #         for entry in entries:
            #             if entry.is_file() and not entry.name == ('.DS_Store') and not new_name.lower().endswith('.png'):
            #                 print('Now about to check exif for: ', entry.name)
            #                 with open(entry, 'rb') as image_file:
            #                     my_image = Image(image_file)
            #                     print(my_image.model)
            #                     fold_struc = fold_struc + my_image.model
            #                     os.makedirs(p.date.strftime(fold_struc), exist_ok=True)
            #                     tar_dir = p.date.strftime(fold_struc) + '/'
            #                     shutil.move(prep_dir_str + '/' + entry.name, tar_dir)
        i += 1



    os.system('echo ' + str(today) + ': ' + str(i) + ' files. >> log.txt')



def conversion(photo_dir):
    basepath = photo_dir
    with os.scandir(basepath) as entries:
        for entry in entries:
            photofile = entry.name
            print('entry: ', photofile)
            if entry.name.lower().endswith('.heic'):      
                # print('start converting of ', photofile)
                base = os.path.splitext(photofile)[0]
                new_name_jpg = str(base + '.jpg')
                # print('Original file in: ' ,basepath + '/' + photofile)
                # print('to: ' ,photo_dir + '/' + new_name_jpg)
                converter = ImageConverter()
                input = photo_dir + '/' + photofile
                output = photo_dir + '/' + str(new_name_jpg)
                converter.write_jpeg(input, output)
                os.remove(input)
                print('removed org heic file!')

               

if __name__ == "__main__":
    main()
