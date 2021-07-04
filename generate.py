from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os.path,os,json

def convert_to_degrees(value):
        return float(value[0]) + (float(value[1]) / 60.0) + (float(value[2]) / 3600.0)

# From https://sylvaindurand.org/gps-data-from-photos-with-python/
def get_gps(exif):
  gps,date = {},None
  
  for key, value in exif.items():
    name = TAGS.get(key, key)
    print(name)
    if name == "GPSInfo":
      gps_exif = exif[key]
      for k in gps_exif.keys():
        name = GPSTAGS.get(k,k)
        gps[name] = gps_exif[k]
    elif name == "DateTime":
      date = exif[key]
  print(gps,date)
  lat = convert_to_degrees(gps['GPSLatitude']) * (gps['GPSLatitudeRef'] == 'S' and -1 or 1)
  lng = convert_to_degrees(gps['GPSLongitude']) * (gps['GPSLongitudeRef'] == 'W' and -1 or 1)
  alt = float(gps['GPSAltitude'])
  return lat,lng,alt,date

def gen_features():
  features = []
  for d in os.listdir('images'):
    for i in os.listdir(os.path.join('images',d)):
      img = Image.open(os.path.join('images',d,i))
      exif = img._getexif()
      lat,lng,alt,date = get_gps(exif)
      print(lat,lng,alt)
      features.append({
        "type":"Feature",
        "properties": {
            "name": i,
            "amenity": "Location",
            "popupContent": "%s: %s",
            "imageUrl": os.path.join('/images',d,i),
            "label": d,
            "altitude": alt,
            "date": date,
        },
        "geometry": {
            "type": "Point",
            "coordinates": [lng,lat]
        }
      })
  return features

if __name__=="__main__":
  with open("features.json","w") as f:
    features = gen_features()
    f.write(json.dumps(features,indent=1))
    print("Wrote %i features to features.json" % len(features))

