import osxphotos
import datetime
import os

from datetime import date, timedelta

def main():


    # This is yesterday's date - relevant for daily exports
    today = date.today()
    yesterday = today - timedelta(days = 1)
    yes_str = yesterday.strftime('%Y%m%d')

    # Start exporting photos from this date onwards
    yes_str = '20200101'

    photosdb = osxphotos.PhotosDB()
    photos = photosdb.photos(from_date=datetime.datetime.strptime(yes_str, '%Y%m%d'))


    for p in photos:
           # The folder structure - right now it is root / year / month
        fold_struc = "export/%Y/%m/" + str(p.exif_info.camera_model)

        os.makedirs(p.date.strftime(fold_struc), exist_ok=True)

        if p.hasadjustments:
            p.export(p.date.strftime(fold_struc), p.date.strftime('%Y%m%d') + '_' +str(p.exif_info.camera_model) + '_' + p.original_filename, edited=True)
        else:
            p.export(p.date.strftime(fold_struc), p.date.strftime('%Y%m%d') + '_' + str(p.exif_info.camera_model) + '_' + p.original_filename)

        # print(
        #     p.original_filename,
        #     p.date.strftime('%Y%m%d'),
        #     file_extension,
        #     p.date.strftime('%Y%m%d') + str(file_extension)
        # )

if __name__ == "__main__":
    main()