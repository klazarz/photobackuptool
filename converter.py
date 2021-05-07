import osxphotos
import datetime
import os

from osxphotos.imageconverter import ImageConverter


def main():

    converter = ImageConverter()
    converter.write_jpeg('/Users/klazarz/Desktop/tmp/20210403_IMG_0045.HEIC','/Users/klazarz/Desktop/tmp/20210403_IMG_0045.jpg')
    
    # osxphotos.fileutil.FileUtilMacOS.convert_to_jpeg('/Volumes/YOGI/tmp/tmp/20210403_IMG_0045.HEIC','/Volumes/YOGI/tmp/tmp/20210403_IMG_0045.jpg')
  
if __name__ == "__main__":
    main()
