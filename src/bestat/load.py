import os
from django.contrib.gis.utils import LayerMapping
from .models import Neighbor

ls = []
for a, b, c in os.walk("bestat"):
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


