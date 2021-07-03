from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os.path,os


def gen():
  for d in os.listdir('images'):
    for i in os.listdir(os.path.join('images',d)):
      img = Image.open(os.path.join('images',d,i))
      exif = img.getexif()
      print(i,exif)

if __name__=="__main__":
  gen()

