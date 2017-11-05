import os
from django.contrib.gis.utils import LayerMapping
from .models import Neighbor,Zipcode,City
import json

ls = []
for a, b, c in os.walk("bestat/data/region"):
    ls.extend([os.path.join(a,i) for i in c if i.endswith("shp")])

neighbor_mapping = {
    'state' : 'State',
    'county' : 'County',
    'city' : 'City',
    'name' : 'Name',
    'regionid' : 'RegionID',
    'geom' : 'MULTIPOLYGON',
}

def run(verbose=True):
    for worldshp in ls:
        lm = LayerMapping(Neighbor, worldshp, neighbor_mapping, transform=False )
        lm.save(strict=True, verbose=verbose)

zipshp = "/home/liuziqicmu/testpis/zip/tl_2015_us_zcta510.shp"

zipcode_mapping = {
    'zcta5ce10' : 'ZCTA5CE10',
    'geoid10' : 'GEOID10',
    'classfp10' : 'CLASSFP10',
    'mtfcc10' : 'MTFCC10',
    'funcstat10' : 'FUNCSTAT10',
    'aland10' : 'ALAND10',
    'awater10' : 'AWATER10',
    'intptlat10' : 'INTPTLAT10',
    'intptlon10' : 'INTPTLON10',
    'geom' : 'MULTIPOLYGON',
}
def runzip(verbose=True):
    lm = LayerMapping(Zipcode, zipshp, zipcode_mapping, transform=False )
    lm.save(strict=True, verbose=verbose)

def getcity():
    jsonf = open("bestat/data/city/cities.json", "r")
    jsonr = jsonf.read()
    cityjson = json.dumps(jsonr)
    for i, items in enumerate(cityjson):
        c = City(name=cityjson[i]['city'],
                 point='POINT(' + str(cityjson[i]['longitude']) + ' ' + str(cityjson[i]['latitude']) + ')',
                 population=int(cityjson[i]['population']), activate=0)
        c.save()
