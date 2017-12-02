# encoding: utf-8

'''

@author: David


@file: picture.py

@time:

@desc:
'''

from api.GooglePlaces import GooglePlaces, types, GooglePlacesError
import requests
from io import BytesIO
from PIL import Image
import os


class Picture(object):
    _url = "https://maps.googleapis.com/maps/api/streetview?size={}&location={}&heading=90&pitch=10&key={}"
    _placeurl = "https://maps.googleapis.com/maps/api/place/photo?maxwidth={}&photoreference={}&key={}&maxheight={}"
    _key = "AIzaSyAQi5ECDVGwZ6jpPShEjL1GbLZBvDlee8c"

    def __init__(self, key):
        self._key = key

    def find_picture(self, loc, size="500x400"):
        address = "/static/img/region/" + loc.replace(" ", "_") + ".png"
        cnt = 0
        if os.path.isfile("bestat" + address):
            print("find")
            return address
        else:
            address = self.get_picture(loc, size)

        return address

    def get_picture(self, loc, size="500x400"):
        try:
            gp = GooglePlaces(api_key=self._key)
            results = gp.text_search(query=loc)
            photo_place = results.places[0].photos
            if len(photo_place) != 0:
                print(size.split("x"))
                width = size.split("x")[0]
                height = size.split("x")[1]
                res = requests.get(self._placeurl.format(width, photo_place[0].photo_reference, self._key, height),
                                   stream=True)

            else:
                raw = results.raw_response
                coor = str(raw['results'][0]['geometry']['viewport']['northeast']['lat']) + "," + str(
                    raw['results'][0]['geometry']['viewport']['northeast']['lng'])

                res = requests.get(self._url.format(size, coor, self._key), stream=True)
            if res.status_code != 200:
                return "/static/img/region/Shadyside_Pittsburgh.png"
            i = Image.open(BytesIO(res.content))
            i.save("bestat/static/img/region/" + loc.replace(" ", "_") + ".png")
            return "/static/img/region/" + loc.replace(" ", "_") + ".png"
        except Exception as e:
            print(e)
            return "/static/img/region/NA.png"
