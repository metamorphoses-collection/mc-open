#!/usr/bin/env python3
"""Build a Paestum GIS: a QGIS-openable GeoPackage in UTM 33N (EPSG:32633) plus a
georeferenced GeoTIFF of the Greco-Theodorescu 'Plan d'ensemble' and a rendered map.

Layers (all EPSG:32633):
  walls, gates, monuments, streets   -- from OpenStreetMap (c OSM contributors, ODbL)
  enceinte_hull                      -- convex hull of the wall trace (area/circuit check)
Raster:
  greco_fig1_georef.tif              -- CRAI 1994 Fig.1 registered on the 4 gates (WORKING layer; copyright EFR)
Outputs -> reference/paestum_gis/
"""
import ocsi_paths
import json, math, os
import numpy as np
from pyproj import Transformer
from shapely.geometry import LineString, Point, Polygon, mapping
from shapely.ops import unary_union
import geopandas as gpd
import rasterio
from rasterio.control import GroundControlPoint
from rasterio.transform import from_gcps
from PIL import Image

GIS=ocsi_paths.at("reference/paestum_gis"); os.makedirs(GIS,exist_ok=True)
UTM="EPSG:32633"
tf=Transformer.from_crs("EPSG:4326",UTM,always_xy=True)
def utm(lon,lat): return tf.transform(lon,lat)

feat=json.load(open(f"{GIS}/paestum_osm_features.json"))['elements']
street=json.load(open(f"{GIS}/paestum_osm_streets.json"))['elements']

def geom_utm(e): return [utm(p['lon'],p['lat']) for p in e['geometry']]

# ---- vector layers ----
walls=[LineString(geom_utm(e)) for e in feat if e.get('tags',{}).get('barrier')=='city_wall']
gdf_walls=gpd.GeoDataFrame({'kind':['city_wall']*len(walls)},geometry=walls,crs=UTM)

gate_rows=[]
for e in feat:
    t=e.get('tags',{})
    if e['type']=='node' and t.get('historic')=='city_gate':
        gate_rows.append((t.get('name','gate'),Point(utm(e['lon'],e['lat']))))
# infer Aurea (N) & Giustizia (S) from wall extremes near central x
allpts=[p for w in walls for p in w.coords]
xs=[p[0] for p in allpts]; ys=[p[1] for p in allpts]; cx=(min(xs)+max(xs))/2
north=max((p for p in allpts if abs(p[0]-cx)<300),key=lambda p:p[1])  # UTM y up = north
south=min((p for p in allpts if abs(p[0]-cx)<300),key=lambda p:p[1])
gate_rows += [('Porta Aurea (N)*',Point(north)),('Porta Giustizia (S)*',Point(south))]
gdf_gates=gpd.GeoDataFrame({'name':[n for n,_ in gate_rows]},geometry=[g for _,g in gate_rows],crs=UTM)

FUNC={'Tempio di Athena':'religious','Tempio di Hera II - di Nettuno':'religious','Tempio di Hera I - Basilica':'religious',
 'Tempio di Mens Bona':'religious','Northern sanctuary':'religious','Sanctuary with a pool':'religious','Sanctuary of Santa Venera':'religious',
 'Ekklesiasterion':'civil','Comitium':'civil','Basilica romana':'civil','Macellum':'civil','Anfiteatro':'civil','Shops':'civil',
 'Casa con peristilio':'residential','Casa con impluvio di marmo':'residential','Giardino romano':'residential'}
PERIOD={'Tempio di Hera I - Basilica':'Greek','Tempio di Hera II - di Nettuno':'Greek','Tempio di Athena':'Greek','Ekklesiasterion':'Greek',
 'Tempio di Mens Bona':'Greek','Northern sanctuary':'Greek','Sanctuary with a pool':'Greek','Comitium':'Republican','Macellum':'Republican',
 'Basilica romana':'Republican','Shops':'Republican','Casa con peristilio':'Roman','Casa con impluvio di marmo':'Roman',
 'Giardino romano':'Roman','Anfiteatro':'Imperial','Sanctuary of Santa Venera':'Greek-Roman'}
mons=[]
for e in feat:
    t=e.get('tags',{}); nm=t.get('name','')
    if nm in FUNC and e.get('geometry') and e['type']=='way':
        g=geom_utm(e)
        if len(g)>=3: mons.append((nm,FUNC[nm],PERIOD.get(nm,'Roman'),Polygon(g)))
gdf_mons=gpd.GeoDataFrame({'name':[m[0] for m in mons],'function':[m[1] for m in mons],'period':[m[2] for m in mons]},
                          geometry=[m[3] for m in mons],crs=UTM)
# buildings (excavated house-walls) + museum (modern) from the buildings pull
import os as _os
bld=json.load(open(f"{GIS}/paestum_osm_buildings.json"))['elements'] if _os.path.exists(f"{GIS}/paestum_osm_buildings.json") else []
sitepoly=[Polygon(geom_utm(e)) for e in feat if e.get('tags',{}).get('name','').startswith('Sito')]
from shapely.prepared import prep as _prep
psite=_prep(sitepoly[0].buffer(40)) if sitepoly else None
bpolys=[]; mus=[]
for e in bld:
    if e['type']!='way' or 'geometry' not in e or len(e['geometry'])<3: continue
    nm=e.get('tags',{}).get('name',''); poly=Polygon(geom_utm(e))
    if 'muse' in nm.lower() or e.get('tags',{}).get('tourism')=='museum': mus.append((nm or 'Museo',poly)); continue
    if psite and psite.intersects(poly.centroid): bpolys.append(poly)
gdf_bld=gpd.GeoDataFrame({'kind':['excavated']*len(bpolys)},geometry=bpolys,crs=UTM) if bpolys else None
gdf_mus=gpd.GeoDataFrame({'name':[m[0] for m in mus],'era':['modern']*len(mus)},geometry=[m[1] for m in mus],crs=UTM) if mus else None

# the collection's geotagged photos -> point layer (UTM), with file path so QGIS can preview them
import glob as _glob
from PIL import Image as _Image, ExifTags as _Exif
from shapely.geometry import Point as _Point
_GPS=next(k for k,v in _Exif.TAGS.items() if v=='GPSInfo')
def _dms(v,r): d=float(v[0])+float(v[1])/60+float(v[2])/3600; return -d if r in ('S','W') else d
_TRIP=_os.path.expanduser(os.environ.get("PAESTUM_PHOTOS", "photos"))
prows=[]
for f in sorted(_glob.glob(_TRIP+"/*.jpeg")):
    try:
        ex=_Image.open(f)._getexif() or {}; g=ex.get(_GPS)
        if not (g and 2 in g and 4 in g): continue
        lat=_dms(g[2],g.get(1,'N')); lon=_dms(g[4],g.get(3,'E'))
        date=ex.get(36867) or ex.get(306) or ''
        prows.append((_os.path.basename(f), f, str(date), lat, lon, _Point(utm(lon,lat))))
    except Exception: pass
gdf_ph=gpd.GeoDataFrame({'file':[p[0] for p in prows],'path':[p[1] for p in prows],'date':[p[2] for p in prows],
                         'lat':[p[3] for p in prows],'lon':[p[4] for p in prows]},
                        geometry=[p[5] for p in prows],crs=UTM) if prows else None

st=[LineString(geom_utm(e)) for e in street if e['type']=='way' and e.get('geometry') and len(e['geometry'])>1]
gdf_st=gpd.GeoDataFrame({'kind':['path']*len(st)},geometry=st,crs=UTM)

hull=unary_union(walls).convex_hull
gdf_hull=gpd.GeoDataFrame({'area_ha':[hull.area/1e4],'perim_m':[hull.length]},geometry=[hull],crs=UTM)

gpkg=f"{GIS}/paestum.gpkg"
if os.path.exists(gpkg): os.remove(gpkg)
gdf_walls.to_file(gpkg,layer='walls',driver='GPKG')
gdf_gates.to_file(gpkg,layer='gates',driver='GPKG')
gdf_mons.to_file(gpkg,layer='monuments',driver='GPKG')
gdf_st.to_file(gpkg,layer='streets',driver='GPKG')
gdf_hull.to_file(gpkg,layer='enceinte_hull',driver='GPKG')
if gdf_bld is not None: gdf_bld.to_file(gpkg,layer='buildings',driver='GPKG')
if gdf_mus is not None: gdf_mus.to_file(gpkg,layer='museum_modern',driver='GPKG')
if gdf_ph is not None: gdf_ph.to_file(gpkg,layer='my_photos',driver='GPKG'); print("my_photos layer: %d points"%len(gdf_ph))
print("GeoPackage:",gpkg,"| hull %.1f ha / %.0f m | monuments w/ function+period | buildings %d"%(hull.area/1e4,hull.length,len(bpolys)))
# (Greco raster georeferencing removed 2026-07-20 — the plate is a printed reference, cited in the
#  bibliography, not carried as data; the phasing lives in the monuments' 'period' attribute.)
