import os
import sys
import time
import exifread
from pymediainfo import MediaInfo
from PyPDF2 import PdfReader

def print_media_metadata(file_path):
    try:
        media_info = MediaInfo.parse(file_path)
        for track in media_info.tracks:
            for key, value in track.to_data().items():
                print(f"{key}: {value}")
    except Exception as e:
        print(f"Error: {e}")

def print_exif_metadata(file_path):
    def get_if_exist(data, key):
        return data[key] if key in data else None

    def convert_to_degrees(value):
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)
        return d + (m / 60.0) + (s / 3600.0)

    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
            for tag in tags.keys():
                print(f"EXIF TAG {tag}: {tags[tag]}")            

            lat_ref = get_if_exist(tags, 'GPS GPSLatitudeRef')
            lat = get_if_exist(tags, 'GPS GPSLatitude')
            lon_ref = get_if_exist(tags, 'GPS GPSLongitudeRef')
            lon = get_if_exist(tags, 'GPS GPSLongitude')
            if lat and lon and lat_ref and lon_ref:
                lat = convert_to_degrees(lat)
                if lat_ref.values[0] != 'N':
                    lat = -lat
                lon = convert_to_degrees(lon)
                if lon_ref.values[0] != 'E':
                    lon = -lon
                print(f"=====Geolocation: Latitude: {lat}, Longitude: {lon}")
    except Exception as e:
        print(f"Error: {e}")

def print_pdf_metadata(file_path):
    try:
        reader = PdfReader(file_path)
        info = reader.metadata
        for key, value in info.items():
            print(f"{key}: {value}")

        if info.title:
            print(f"=====Tittle: {info.title}")
        if info.subject:
            print(f"=====Subject}: {info.subject}")
        if info.keywords:
            print(f"=====Keywords: {info.keywords}")
        if info.producer:
            print(f"=====Produ.: {info.producer}")
        if info.creation_date:
            print(f"=====creation date: {info.creation_date}")
        if info.modification_date:
            print(f"=====modification date: {info.modification_date}")
        if info.author:
            print(f"=====Author: {info.author}")
        if info.creator:
            print(f"=====Ceiator: {info.creator}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python script.py <file>")
        sys.exit(1)

    file_path = sys.argv[1]
    print_media_metadata(file_path)
    if file_path.lower().endswith(('.jpg', '.jpeg', '.png', 'webp', 'avif')):
        print_exif_metadata(file_path)
    elif file_path.lower().endswith('.pdf'):
        print_pdf_metadata(file_path)
