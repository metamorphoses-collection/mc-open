#!/usr/bin/env python3
"""Render a publication map from the Paestum GIS (EPSG:32633):
Greco Fig.1 (georeferenced, faded) under the OSM vector layers, with UTM grid, scale bar,
north arrow, legend and source attribution. Output: reference/paestum_gis/paestum_gis_map.png
"""
import ocsi_paths
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow
import geopandas as gpd, rasterio
from rasterio.plot import show as rshow

GIS=ocsi_paths.at("reference/paestum_gis")
walls=gpd.read_file(f"{GIS}/paestum.gpkg",layer="walls")
gates=gpd.read_file(f"{GIS}/paestum.gpkg",layer="gates")
mons=gpd.read_file(f"{GIS}/paestum.gpkg",layer="monuments")
streets=gpd.read_file(f"{GIS}/paestum.gpkg",layer="streets")
hull=gpd.read_file(f"{GIS}/paestum.gpkg",layer="enceinte_hull")

fig,ax=plt.subplots(figsize=(15,11))
with rasterio.open(f"{GIS}/greco_fig1_georef.tif") as r:
    rshow(r,ax=ax,cmap="gray",alpha=0.5,zorder=1)
streets.plot(ax=ax,color="#b9a877",lw=0.5,zorder=2)
hull.boundary.plot(ax=ax,color="#7c6a48",lw=1,ls="--",zorder=3)
walls.plot(ax=ax,color="#b0341f",lw=2.4,zorder=5)
mons.plot(ax=ax,facecolor="#d8b58a",edgecolor="#6f4f2a",lw=0.8,alpha=0.9,zorder=4)
# label the headline monuments
KEY={"Tempio di Hera II - di Nettuno":"Hera II ‘Neptune’","Tempio di Hera I - Basilica":"Hera I (Basilica)",
     "Anfiteatro":"Amphitheatre","Northern sanctuary":"Athena (N sanct.)","Comitium":"Comitium",
     "Ekklesiasterion":"Bouleuterion","Macellum":"Macellum","Basilica romana":"Basilica"}
for _,row in mons.iterrows():
    nm=KEY.get(row["name"])
    if nm:
        c=row.geometry.centroid; ax.annotate(nm,(c.x,c.y),fontsize=7.5,ha="center",color="#3a2c18",
            path_effects=None,zorder=7,bbox=dict(boxstyle="round,pad=0.1",fc="white",ec="none",alpha=0.6))
for _,row in gates.iterrows():
    p=row.geometry; ax.plot(p.x,p.y,"o",ms=8,mfc="white",mec="#b0341f",mew=2,zorder=6)
    ax.annotate(row["name"].replace(" (N)*"," N").replace(" (S)*"," S"),(p.x,p.y),fontsize=8,color="#b0341f",
                xytext=(6,4),textcoords="offset points",zorder=7,fontweight="bold")
# extent = enceinte + margin
minx,miny,maxx,maxy=hull.total_bounds; pad=120
ax.set_xlim(minx-pad,maxx+pad); ax.set_ylim(miny-pad,maxy+pad); ax.set_aspect("equal")
# scale bar (500 m, real UTM metres)
x0=minx+60; y0=miny-pad+70
ax.plot([x0,x0+500],[y0,y0],color="black",lw=3,zorder=8)
ax.plot([x0,x0],[y0-8,y0+8],color="black",lw=3); ax.plot([x0+500,x0+500],[y0-8,y0+8],color="black",lw=3)
ax.text(x0+250,y0+14,"500 m",ha="center",fontsize=9,zorder=8)
# north arrow (UTM grid north = up)
ax.annotate("N",xy=(maxx-40,maxy-40),xytext=(maxx-40,maxy-150),ha="center",fontsize=13,fontweight="bold",
            arrowprops=dict(arrowstyle="-|>",color="black",lw=2),zorder=8)
ax.set_title("PAESTUM · POSEIDONIA — GIS (EPSG:32633 / UTM 33N)\n"
             "OSM vectors (walls · gates · monuments · streets) over the georeferenced Greco–Theodorescu Plan d'ensemble",
             fontsize=13)
ax.set_xlabel("UTM easting (m)"); ax.set_ylabel("UTM northing (m)"); ax.grid(True,lw=0.3,alpha=0.4)
ax.text(0.5,-0.075,"Vectors © OpenStreetMap contributors (ODbL). Raster: Greco & Theodorescu / Greco 1994, CRAI (École française de Rome) — WORKING layer, "
        "georeferenced on the 4 gates; not for publication. Reproj. UTM 33N.",transform=ax.transAxes,ha="center",fontsize=7.5,color="#555")
plt.tight_layout(); plt.savefig(f"{GIS}/paestum_gis_map.png",dpi=130,bbox_inches="tight")
print("wrote",f"{GIS}/paestum_gis_map.png")
