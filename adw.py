import cx_Oracle
import osxphotos
import datetime
import os
import json
import adbsettings

from datetime import date, timedelta
from exif import Image


def main():
    photosdb = osxphotos.PhotosDB()
    # photos = photosdb.photos(from_date=datetime.datetime.strptime(yes_str, '%Y%m%d'))
    photos = photosdb.photos()

    cx_Oracle.init_oracle_client(lib_dir="/Users/kevin/instantclient_19_8/")

    connection = cx_Oracle.connect(user=adbsettings.user, password=adbsettings.password, dsn=adbsettings.dwh)

    cursor = connection.cursor()

    i = 0
    k = 1

    for p in photos: 
        if  not p.shared or p.shared == None:
            new_name = p.date.strftime('%Y%m%d') + '_' + p.original_filename

            # print('location ', p.location)

            print('Inserted file', new_name, ' number :', i, ' Batch', k)

            exif_value = p.exiftool.json().decode('utf8').replace("'", '"').replace("\\","")
            photo_value = p.json()
        
            try:
                exif_verify = json.loads(exif_value)
            except ValueError as e:
                exif_value = '{"NoExif": "None"}'

            try:
                photo_verify = json.loads(photo_value)
            except ValueError as e:
                photo_value = '{"NoExif": "None"}'

                
            # if p.exif_info:
            #     exif_value = p.exiftool.json().decode('utf8').replace("'", '"').replace("\\","")
            # else:
            #     exif_value = '{"NoExif": "None"}'


            # var = cursor.var(cx_Oracle.DB_TYPE_JSON)
            # var.setvalue(0, exif_value)

            cursor.execute("insert into photos(uuid,creation_date,filename,exiftool,photojson,location,make, model) values (:uui, :creation_date, :filename, :exiftool, :photojson, :location, :make, :model)", uui = p.uuid, creation_date = p.date, filename = new_name, exiftool = exif_value, photojson = photo_value, location = str(p.location), make=p.exif_info.camera_make, model=p.exif_info.camera_model)


            
            
            i += 1

         
            if i==1000:
                connection.commit() 
                i=0
                k += 1
    
    connection.commit() 


if __name__ == "__main__":
    main()
