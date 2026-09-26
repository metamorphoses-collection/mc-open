# Paestum GIS

A georeferenced GIS of ancient Paestum (Poseidonia) in **EPSG:32633 (UTM zone 33 N)** — true projected metres.

## Contents
| file | what | source / licence |
|---|---|---|
| `paestum.gpkg` | GeoPackage, 5 layers: `walls` · `gates` · `monuments` · `streets` · `enceinte_hull` | © OpenStreetMap contributors, **ODbL** |
| `paestum_osm_features.json` / `_streets.json` | raw OSM (Overpass) pulls | ODbL |
| *(not included)* `greco_fig1_georef.tif` | Greco–Theodorescu *Plan d'ensemble* (CRAI 1994 Fig. 1) georeferenced on the 4 gates | raster © **École française de Rome** — **working layer, NOT for publication** |


## Rebuild
```
python3 pipeline/build_paestum_gis.py       # OSM -> UTM 33N GeoPackage + georeferenced GeoTIFF
python3 pipeline/render_paestum_gis_map.py  # publication map
```
Stack: `geopandas · rasterio · shapely · pyproj · pyogrio · matplotlib` (Python).

## Interactive web map (no install)
`paestum_webmap.html` — self-contained Leaflet map; **double-click → browser**. Satellite / OSM basemaps
(the imagery *is* the architectural plan: house walls + streets) with toggleable layers:
- city walls & gates · **monuments coloured by function** (religious / civil / residential) · Athena temple
- **excavated building footprints** (55 house-wall polygons, OSM) · **Museo flagged modern** · streets · Forum/Agora labels
- **📷 collection photographs (July 2025)** — 38 GPS-placed markers with embedded thumbnails (click to view)
Build: `python3 pipeline/build_paestum_webmap.py`. Photographs: Metamorphoses of Civilization collection (July 2025), CC BY 4.0; vectors © OpenStreetMap contributors (ODbL); imagery Esri.

## Open in QGIS
Add `paestum.gpkg` (all layers) and `greco_fig1_georef.tif`; project CRS = EPSG:32633.

## Measurements (UTM 33 N, verified)
- enceinte convex hull: **129.6 ha**, perimeter **4 467 m** (brackets the sourced ~120 ha / ~4.75 km circuit)
- extent **1 576 m (E–W) × 1 040 m (N–S)** — the city is **wider E–W**; the temple spine (Athena → forum → Hera) is the short N–S axis
- Hera II "Neptune" 63×29 m · Hera I "Basilica" 56×28 m · amphitheatre 40×62 m (W half excavated)

## Provenance rule
OSM vectors are the accurate georeferenced base. The Greco raster is a **working underlay** for tracing/validation only — anything we *publish* stays our own vectors (same rule as Golvin). Temple/forum dimensions per Greco–Theodorescu & the excavation literature.

## Known limits / next
- Raster registration ~50 m (four hand-picked gate control points) — **tighten** by re-picking gates precisely.
- **Insula grid** not yet a vector layer (visible in the raster) — digitize the plateiai/stenopoi + western insulae from Fig. 1 into a `grid` layer via the affine transform.
- Fig. 2 (agora, period-phased) not yet georeferenced — add as `agora_phased` with Greek/Lucanian/Republican/Imperial attributes.


**This public copy** contains the OSM-derived vector layers, the raw OSM pulls, the web map and the build scripts. The Greco–Theodorescu raster (© École française de Rome) is a private working layer and is not included.
