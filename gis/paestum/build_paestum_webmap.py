#!/usr/bin/env python3
"""Interactive Paestum web map (Leaflet, self-contained), ALL LABELS IN ENGLISH.
Layers: satellite/OSM base · walls · 4 gates + towers · Via Sacra + Decumanus · monuments
(polygons + points) coloured by FUNCTION and by PERIOD · ancient house-wall footprints ·
Museo (modern) · the collection's 38 geotagged photos · Wikimedia CC photos (site + per-monument for the
ekklesiasterion & comitium) · Greco Fig.2 (agora, phased) raster overlay with opacity slider.
Output: reference/paestum_gis/paestum_webmap.html
"""
import ocsi_paths
import json, glob, os, io, base64
from PIL import Image, ImageOps, ExifTags
from shapely.geometry import Polygon
from shapely.prepared import prep
GIS=ocsi_paths.at("reference/paestum_gis")
feat=json.load(open(f"{GIS}/paestum_osm_features.json"))['elements']
bld=json.load(open(f"{GIS}/paestum_osm_buildings.json"))['elements']
extra=json.load(open(f"{GIS}/paestum_osm_extra.json"))['elements']
st=json.load(open(f"{GIS}/paestum_osm_streets.json"))['elements']
wiki=json.load(open(f"{GIS}/wikimedia_photos.json"))
monpix=json.load(open(f"{GIS}/wikimedia_monument_photos.json"))
redis=json.load(open(f"{GIS}/rediscovery_views.json"))
recon=json.load(open(f"{GIS}/reconstruction_views.json"))

# Italian -> English label
EN={'Tempio di Athena':'Temple of Athena','Tempio di Hera II - di Nettuno':'Temple of Hera II (“Neptune”)',
 'Tempio di Hera I - Basilica':'Temple of Hera I (Basilica)','Tempio di Mens Bona':'Temple of Mens Bona',
 'Anfiteatro':'Amphitheatre','Ekklesiasterion':'Ekklesiasterion','Comitium':'Comitium','Macellum':'Macellum',
 'Basilica romana':'Roman Basilica','Giardino romano':'Roman Garden','Casa con peristilio':'Peristyle House',
 'Casa con impluvio di marmo':'House with Marble Impluvium','Shops':'Shops','Sanctuary with a pool':'Sanctuary with a Pool',
 'Northern sanctuary':'Northern Sanctuary (Athena)','Sanctuary of Santa Venera':'Sanctuary of Santa Venera','Heroon':'Heroon',
 'Piscina ellenistica':'Hellenistic Pool','Asklepion':'Asclepieion','Casa dei sacerdoti':'House of the Priests',
 'Orologio ad acqua':'Water Clock','Tempio di Mater Matuta':'Temple of Mater Matuta','Tempio di Magna Mater':'Temple of Magna Mater (Cybele)',
 'Tempio di Demetra':'Temple of Demeter','Altare del tempio di Nettuno':'Altar of the Temple of Neptune',
 'Altare romano del tempio di Nettuno':'Roman Altar of the Temple of Neptune','Altare del tempio di Hera':'Altar of the Temple of Hera',
 'Altare del tempio di Atena':'Altar of the Temple of Athena','Foro':'Forum','Colonna dorica':'Doric Column',
 'Torre Laura':'Tower “Laura”','Torre 28':'Tower 28','Via Sacra':'Via Sacra (Sacred Way)','Decumano':'Decumanus',
 'Museo archeologico nazionale di Paestum':'National Archaeological Museum','Porta Marina':'Porta Marina (Sea Gate · W)','Porta Sirena':'Porta Sirena (E)'}
FUNC={'Temple of Athena':'religious','Temple of Hera II (“Neptune”)':'religious','Temple of Hera I (Basilica)':'religious',
 'Temple of Mens Bona':'religious','Northern Sanctuary (Athena)':'religious','Sanctuary with a Pool':'religious',
 'Sanctuary of Santa Venera':'religious','Hellenistic Pool':'religious','Asclepieion':'religious','House of the Priests':'religious',
 'Temple of Mater Matuta':'religious','Temple of Magna Mater (Cybele)':'religious','Temple of Demeter':'religious',
 'Altar of the Temple of Neptune':'religious','Roman Altar of the Temple of Neptune':'religious','Altar of the Temple of Hera':'religious',
 'Altar of the Temple of Athena':'religious','Doric Column':'religious','Heroon':'religious',
 'Ekklesiasterion':'civil','Comitium':'civil','Roman Basilica':'civil','Macellum':'civil','Amphitheatre':'civil','Shops':'civil',
 'Forum':'civil','Water Clock':'civil','Peristyle House':'residential','House with Marble Impluvium':'residential','Roman Garden':'residential'}
PERIOD={'Temple of Hera I (Basilica)':'Greek','Temple of Hera II (“Neptune”)':'Greek','Temple of Athena':'Greek','Ekklesiasterion':'Greek',
 'Temple of Mens Bona':'Greek','Northern Sanctuary (Athena)':'Greek','Sanctuary with a Pool':'Greek','Hellenistic Pool':'Greek',
 'Temple of Demeter':'Greek','Temple of Mater Matuta':'Greek','Doric Column':'Greek','Heroon':'Greek','Altar of the Temple of Neptune':'Greek',
 'Altar of the Temple of Hera':'Greek','Altar of the Temple of Athena':'Greek','Asclepieion':'Greek→Roman','Sanctuary of Santa Venera':'Greek→Roman',
 'Comitium':'Republican','Macellum':'Republican','Roman Basilica':'Republican','Shops':'Republican','Forum':'Republican',
 'Temple of Magna Mater (Cybele)':'Republican','Roman Altar of the Temple of Neptune':'Republican','Water Clock':'Roman',
 'Peristyle House':'Roman','House with Marble Impluvium':'Roman','Roman Garden':'Roman','Amphitheatre':'Imperial'}
COL={'religious':'#d98a2b','civil':'#3f7fc0','residential':'#5aa14f','modern':'#8a8a8a'}
PCOL={'Greek':'#2b2b2b','Republican':'#3f7fc0','Imperial':'#c0392b','Roman':'#8a6d3b','Greek→Roman':'#7a5a34'}
def en(nm): return EN.get(nm,nm)
def ll(e): return [[p['lon'],p['lat']] for p in e['geometry']]
def fcol(l): return {"type":"FeatureCollection","features":l}
def props(nm,extra_html=""):
    e=en(nm); return {"name":e,"func":FUNC.get(e,'civil'),"period":PERIOD.get(e,'Roman'),"img":extra_html}

# per-monument Wikimedia photo (ekklesiasterion, comitium)
def pick(key):
    for x in monpix.get(key,[]):
        if key in x['title'].lower() or (key=='ekklesiasterion' and 'ekkl' in x['title'].lower()): return x
    return (monpix.get(key) or [None])[0]
ekk=pick('ekklesiasterion'); com=pick('comitium')
def monimg(name):
    x=None
    if name=='Ekklesiasterion': x=ekk
    elif name=='Comitium': x=com
    return ('<br><img src="'+x['thumb']+'"><br><i>'+x['license']+' (Wikimedia)</i>') if x else ''

# polygon monuments (named ways in FUNC)
mons=[]
for n in feat:
    if n['type']=='way' and n.get('geometry') and en(n.get('tags',{}).get('name','')) in FUNC:
        nm=en(n['tags']['name']); p=props(n['tags']['name'],monimg(nm))
        mons.append({"type":"Feature","properties":p,"geometry":{"type":"Polygon","coordinates":[ll(n)]}})
# point monuments (extra nodes)
pmons=[]
for e in extra:
    if e['type']=='node' and e.get('tags',{}).get('historic') in ('archaeological_site','ruins'):
        nm=e['tags'].get('name','')
        if en(nm) in FUNC and en(nm) not in ('Forum',):  # Forum handled as a label
            pmons.append({"type":"Feature","properties":props(nm),"geometry":{"type":"Point","coordinates":[e['lon'],e['lat']]}})
# roads: ALL Via Sacra + Decumanus segments (Via Sacra is split N + S)
roads=[{"type":"Feature","properties":{"name":en(e['tags']['name'])},"geometry":{"type":"LineString","coordinates":ll(e)}}
       for e in extra if e['type']=='way' and e.get('tags',{}).get('name') in ('Via Sacra','Decumano') and e.get('geometry')]
# amphitheatre: reconstructed EASTERN half (mirror the excavated W half across the road axis)
amphr=[]
_amph=[e for e in feat if e['type']=='way' and e.get('tags',{}).get('name')=='Anfiteatro' and e.get('geometry')]
if _amph:
    g=_amph[0]['geometry']; axis=max(p['lon'] for p in g)
    amphr=[{"type":"Feature","properties":{"name":"Amphitheatre — reconstructed eastern half (unexcavated, under the modern road SS18)"},
            "geometry":{"type":"Polygon","coordinates":[[[2*axis-p['lon'],p['lat']] for p in g]]}}]
# towers
def _cen(cs): return [sum(c[0] for c in cs)/len(cs), sum(c[1] for c in cs)/len(cs)]  # tower footprints are tiny -> a marker at the centroid
towers=[{"type":"Feature","properties":{"name":en(e['tags'].get('name','tower'))},"geometry":{"type":"Point","coordinates":_cen(ll(e))}}
        for e in extra if e['type']=='way' and e.get('tags',{}).get('historic')=='tower' and e.get('geometry')]
# gates: 2 OSM nodes + inferred Aurea/Giustizia from wall extremes
gates=[]
for e in feat:
    if e['type']=='node' and e.get('tags',{}).get('historic')=='city_gate':
        gates.append({"type":"Feature","properties":{"name":en(e['tags'].get('name'))},"geometry":{"type":"Point","coordinates":[e['lon'],e['lat']]}})
wp=[(p['lon'],p['lat']) for e in feat if e.get('tags',{}).get('barrier')=='city_wall' for p in e['geometry']]
clon=(min(p[0] for p in wp)+max(p[0] for p in wp))/2
north=max((p for p in wp if abs(p[0]-clon)<0.004),key=lambda p:p[1]); south=min((p for p in wp if abs(p[0]-clon)<0.004),key=lambda p:p[1])
gates.append({"type":"Feature","properties":{"name":"Porta Aurea (N)"},"geometry":{"type":"Point","coordinates":list(north)}})
gates.append({"type":"Feature","properties":{"name":"Porta Giustizia (S)"},"geometry":{"type":"Point","coordinates":list(south)}})
# walls
walls=[{"type":"Feature","properties":{},"geometry":{"type":"LineString","coordinates":ll(e)}} for e in feat if e.get('tags',{}).get('barrier')=='city_wall']
streets=[{"type":"Feature","properties":{},"geometry":{"type":"LineString","coordinates":ll(e)}} for e in st if e['type']=='way' and e.get('geometry') and len(e['geometry'])>1]
# buildings: ancient excavated only (inside site, UNNAMED) — drop modern town + named modern; museum handled apart
site=[e for e in feat if e.get('tags',{}).get('name','').startswith('Sito')][0]
_spoly=Polygon([(p['lon'],p['lat']) for p in site['geometry']]); _xmax=_spoly.bounds[2]
sp=prep(_spoly.buffer(0.0006))
buildings=[]; museum=[]
for e in bld:
    if e['type']!='way' or 'geometry' not in e or len(e['geometry'])<3: continue
    nm=e.get('tags',{}).get('name','')
    if 'muse' in nm.lower() or e.get('tags',{}).get('tourism')=='museum':
        museum.append({"type":"Feature","properties":{"name":'National Archaeological Museum'},"geometry":{"type":"Polygon","coordinates":[ll(e)]}}); continue
    if nm: continue  # named building=yes here = modern (Palazzo De Maria, church, houses)
    c=Polygon([(p['lon'],p['lat']) for p in e['geometry']]).centroid
    if c.x>_xmax: continue  # east of the excavated strip = modern town
    if sp.intersects(c):
        buildings.append({"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[ll(e)]}})
# collection photos
GPSID=next(k for k,v in ExifTags.TAGS.items() if v=='GPSInfo')
def dms(v,r): d=float(v[0])+float(v[1])/60+float(v[2])/3600; return -d if r in('S','W') else d
TRIP=os.path.expanduser(os.environ.get("PAESTUM_PHOTOS", "photos"))
photos=[]
for f in sorted(glob.glob(TRIP+"/*.jpeg")):
    try:
        im=Image.open(f); ex=im._getexif() or {}; g=ex.get(GPSID)
        if not (g and 2 in g and 4 in g): continue
        lat=dms(g[2],g.get(1,'N')); lon=dms(g[4],g.get(3,'E'))
        th=ImageOps.exif_transpose(im); th.thumbnail((260,260)); buf=io.BytesIO(); th.convert("RGB").save(buf,"JPEG",quality=58)
        photos.append({"type":"Feature","properties":{"name":os.path.basename(f),"img":"data:image/jpeg;base64,"+base64.b64encode(buf.getvalue()).decode()},"geometry":{"type":"Point","coordinates":[lon,lat]}})
    except Exception: pass
print("layers: walls %d gates %d towers %d roads %d mon-poly %d mon-pt %d buildings %d museum %d myphotos %d wiki %d"%(
      len(walls),len(gates),len(towers),len(roads),len(mons),len(pmons),len(buildings),len(museum),len(photos),len(wiki)))

T=r'''<!doctype html><html><head><meta charset="utf-8"><title>Paestum — archaeological GIS</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>html,body{height:100%;margin:0}body{display:flex;flex-direction:column}
#map{flex:1 1 auto;min-height:0}
#legendbar{flex:0 0 auto;background:#fffef8;border-top:1px solid #b7a071;padding:5px 12px;font:12px Georgia;color:#3a2c18;display:flex;flex-wrap:wrap;align-items:center;gap:3px 14px}
#legendbar .attrib{color:#8a7a5a;font-size:10.5px;margin-left:auto}
.lbl{font:600 11px Georgia;color:#2a2118;text-shadow:0 0 3px #fff,0 0 3px #fff,0 0 3px #fff;background:none;border:none;box-shadow:none;padding:0}
.rd{font:italic 500 12px Georgia;color:#9a4a1a;text-shadow:0 0 3px #fff,0 0 4px #fff,0 0 4px #fff;background:none;border:none;box-shadow:none;padding:0}
.leaflet-tooltip:before,.leaflet-tooltip-left:before,.leaflet-tooltip-right:before,.leaflet-tooltip-top:before,.leaflet-tooltip-bottom:before{display:none !important;border:none !important}
.big{font:700 13px Georgia;color:#3a2c18;text-shadow:0 0 4px #fff,0 0 4px #fff}
.leg{background:#fffef8;padding:8px 10px;font:12px Georgia;line-height:1.4;border:1px solid #b7a071;border-radius:5px;max-width:235px}
.sw{display:inline-block;width:12px;height:12px;margin-right:5px;vertical-align:middle;border:1px solid #6f5d3d}
.op{background:#fffef8;padding:6px 8px;font:12px Georgia;border:1px solid #b7a071;border-radius:5px}
.leaflet-popup-content{margin:6px}.leaflet-popup-content img{max-width:260px;display:block;cursor:zoom-in}
#lb{display:none;position:fixed;inset:0;background:rgba(0,0,0,.88);z-index:99999;cursor:zoom-out}
#lb img{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);max-width:94vw;max-height:94vh;box-shadow:0 0 40px #000;border:3px solid #fff}
#lb .cap{position:absolute;bottom:14px;left:0;right:0;text-align:center;color:#fff;font:13px Georgia;text-shadow:0 0 6px #000}</style></head>
<body><div id="map"></div>
<div id="legendbar"><b>By function:</b> <span class="sw" style="background:#d98a2b"></span>religious <span class="sw" style="background:#3f7fc0"></span>civil / public <span class="sw" style="background:#5aa14f"></span>residential <span class="sw" style="background:#8a8a8a;border-style:dashed"></span>modern (museum) <span class="attrib">Vectors &copy; OSM (ODbL) · imagery Esri · photographs &copy; Metamorphoses of Civilization collection 2025 · 🌐 CC via Wikimedia · Grand-Tour plates: collection &amp; public domain</span></div>
<div id="lb"><img><div class="cap"></div></div><script>
var walls=__WALLS__,gates=__GATES__,towers=__TOW__,roads=__ROADS__,mons=__MONS__,pmons=__PMONS__,buildings=__BLD__,museum=__MUS__,streets=__ST__,photos=__PH__,wiki=__WIKI__,amphr=__AMPHR__,redis=__REDIS__,recon=__RECON__;
var COL=__COL__,PCOL=__PCOL__;
var sat=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{attribution:'Esri World Imagery',maxZoom:21,maxNativeZoom:19});
var osm=L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'&copy; OpenStreetMap',maxZoom:19});
var map=L.map('map',{layers:[sat]});
var Lst=L.geoJSON(streets,{style:{color:'#ffd98a',weight:1,opacity:0.5}});
var Lb=L.geoJSON(buildings,{style:{color:'#efe4c8',weight:1,fillColor:'#d8c9a0',fillOpacity:0.3}});
var Lrd=L.geoJSON(roads,{style:{color:'#c0651e',weight:3,dashArray:'6 4'},onEachFeature:function(f,l){l.bindTooltip(f.properties.name,{permanent:true,className:'rd'});}}).addTo(map);
var Lw=L.geoJSON(walls,{style:{color:'#ff2a2a',weight:3}}).addTo(map);
function pop(f){return '<b>'+f.properties.name+'</b><br>function: '+f.properties.func+'<br>period: '+f.properties.period+(f.properties.img||'');}
var Lm=L.geoJSON(mons,{style:function(f){return {color:'#4a3a20',weight:1,fillColor:COL[f.properties.func],fillOpacity:0.72};},
   onEachFeature:function(f,l){l.bindTooltip(f.properties.name,{direction:'center',className:'lbl'});l.bindPopup(pop(f));}}).addTo(map);
// phase filters: what STOOD in each civilisation (Greek/Lucanian share standing monuments; Rome adds the civic core)
function mkphase(set){
  var pf=function(f){return set.indexOf(f.properties.period)>=0;};
  var poly=L.geoJSON(mons,{filter:pf,style:function(f){return {color:'#4a3a20',weight:1,fillColor:COL[f.properties.func],fillOpacity:0.78};},onEachFeature:function(f,l){l.bindTooltip(f.properties.name,{direction:'center',className:'lbl'});l.bindPopup(pop(f));}});
  var pt=L.geoJSON(pmons,{filter:pf,pointToLayer:function(f,p){return L.circleMarker(p,{radius:5,color:'#4a3a20',weight:1,fillColor:COL[f.properties.func],fillOpacity:0.9}).bindTooltip(f.properties.name,{direction:'right',className:'lbl'}).bindPopup(pop(f));}});
  return L.layerGroup([poly,pt]);
}
var GK=['Greek','Greek→Roman'];
var LphG=mkphase(GK), LphL=mkphase(GK), LphR=mkphase(['Greek','Greek→Roman','Republican','Imperial','Roman']);
var Lpt=L.geoJSON(pmons,{pointToLayer:function(f,p){return L.circleMarker(p,{radius:5,color:'#4a3a20',weight:1,fillColor:COL[f.properties.func],fillOpacity:0.9}).bindTooltip(f.properties.name,{direction:'right',className:'lbl'}).bindPopup(pop(f));}});
var Lamphr=L.geoJSON(amphr,{style:{color:'#4a90d9',weight:1.5,dashArray:'6 4',fillColor:'#aad4f5',fillOpacity:0.4},onEachFeature:function(f,l){l.bindTooltip('reconstructed half',{direction:'center',className:'lbl'});l.bindPopup(f.properties.name);}});
var Lmus=L.geoJSON(museum,{style:{color:'#555',weight:1.5,dashArray:'5 3',fillColor:'#8a8a8a',fillOpacity:0.55},onEachFeature:function(f,l){l.bindTooltip('Museum (modern)',{direction:'center',className:'lbl'});}});
var Lg=L.geoJSON(gates,{pointToLayer:function(f,p){return L.circleMarker(p,{radius:6,color:'#ff2a2a',fillColor:'#fff',fillOpacity:1,weight:2}).bindTooltip(f.properties.name,{permanent:true,className:'lbl'});}}).addTo(map);
var Ltw=L.geoJSON(towers,{pointToLayer:function(f,p){return L.circleMarker(p,{radius:5,color:'#8a5a2a',fillColor:'#d8b483',fillOpacity:0.9,weight:2}).bindTooltip(f.properties.name,{className:'lbl'});}});
function emojiIcon(em,label,sz){return L.divIcon({className:'',html:'<div role="img" aria-label="'+String(label).replace(/["<>]/g,'')+'" style="font-size:'+sz+'px;filter:drop-shadow(0 0 2px #fff)">'+em+'</div>',iconSize:[sz+2,sz+2],iconAnchor:[(sz+2)/2,(sz+2)/2]});}
var Lph=L.layerGroup(photos.map(function(f){var c=f.geometry.coordinates;return L.marker([c[1],c[0]],{icon:emojiIcon('📷','Photograph: '+f.properties.name,17),title:f.properties.name}).bindPopup('<b>'+f.properties.name+'</b><br><img src="'+f.properties.img+'">',{minWidth:266});}));
var wIcon=L.divIcon({className:'',html:'<div style="font-size:15px;filter:drop-shadow(0 0 2px #fff)">🌐</div>',iconSize:[16,16],iconAnchor:[8,8]});
var wgroups={};
wiki.forEach(function(w){var k=w.lat.toFixed(5)+','+w.lon.toFixed(5);(wgroups[k]=wgroups[k]||[]).push(w);});
var Lwiki=L.layerGroup(Object.keys(wgroups).map(function(k){
  var arr=wgroups[k], c=arr[0];
  var gal=arr.map(function(w){return '<div style="margin-bottom:7px"><a href="'+w.full+'" target="_blank"><img src="'+w.thumb+'"></a><br><span style="font-size:9px;color:#666">'+w.title.slice(0,44)+' · '+w.license+'</span></div>';}).join('');
  var badge=arr.length>1?'<span style="position:absolute;top:-5px;right:-9px;background:#c0392b;color:#fff;border-radius:9px;font:700 9px sans-serif;padding:0 4px">'+arr.length+'</span>':'';
  var icon=L.divIcon({className:'',html:'<div role="img" aria-label="'+arr.length+' Wikimedia photo'+(arr.length>1?'s':'')+' here" style="font-size:16px;filter:drop-shadow(0 0 2px #fff);position:relative">🌐'+badge+'</div>',iconSize:[18,18],iconAnchor:[9,9]});
  return L.marker([c.lat,c.lon],{icon:icon}).bindPopup('<b>'+arr.length+' Wikimedia photo'+(arr.length>1?'s':'')+' here</b><div style="max-height:330px;overflow-y:auto;width:270px;margin-top:4px">'+gal+'</div>');
}));
// Grand-Tour rediscovery views: easel at the viewpoint + arrow to the subject + the plate in the popup
var artIcon=L.divIcon({className:'',html:'<div style="font-size:18px;filter:drop-shadow(0 0 2px #fff)">🖼️</div>',iconSize:[20,20],iconAnchor:[10,10]});
var Lredis=L.layerGroup(redis.map(function(v){
  var line=L.polyline([v.vp,v.subj],{color:'#b07a2a',weight:1.5,dashArray:'4 4',opacity:0.8});
  var m=L.marker(v.vp,{icon:emojiIcon('🖼️','Grand-Tour view: '+v.title+', '+v.artist+' '+v.year,18),title:v.title}).bindPopup('<b>'+(v.id?'<span style="color:#7a5a2a">'+v.id+'</span> · ':'')+v.title+'</b><br><i>'+v.artist+', '+v.year+'</i><br><img src="'+v.img+'"><br><span style="font-size:10px;color:#777">'+v.credit+' · approximate viewpoint (interpretive)</span>',{minWidth:266});
  return L.layerGroup([line,m]);
}));
// Reconstruction views — AI HYPOTHETICAL, one toggleable layer per period, placed at the viewpoint
var reconIcon=L.divIcon({className:'',html:'<div style="font-size:16px;filter:drop-shadow(0 0 2px #fff)">🏛️</div>',iconSize:[18,18],iconAnchor:[9,9]});
function reconLayer(per){return L.layerGroup(recon.filter(function(v){return v.period===per;}).map(function(v){
  return L.marker(v.vp,{icon:emojiIcon('🏛️','Reconstruction: '+v.title+' ('+per+' period, AI hypothetical)',16),title:v.title}).bindPopup('<b>'+v.title+'</b> <span style="font-size:10px;color:#999">('+per+')</span><br><img src="'+v.img+'"><br><span style="font-size:10px;color:#a33">AI hypothetical reconstruction — illustrative, not archaeologically registered'+(v.flagged?' · ⚠ speculative viewpoint':'')+'</span>',{minWidth:266});
}));}
var LrecG=reconLayer('greek'),LrecL=reconLayer('lucanian'),LrecR=reconLayer('roman');
L.control.layers({'Satellite (Esri)':sat,'OpenStreetMap':osm},
  {'City walls':Lw,'Gates':Lg,'Towers':Ltw,'Via Sacra / Decumanus':Lrd,'Monuments — by function':Lm,
   'Phase · Greek Poseidonia (5th c BC)':LphG,'Phase · Lucanian Paestum (4th c BC)':LphL,'Phase · Roman Paestum':LphR,
   'Altars &amp; minor monuments (points)':Lpt,'Amphitheatre — reconstructed half':Lamphr,'Excavated house-walls':Lb,'Museum (modern)':Lmus,'Streets / paths':Lst,
   ['📷 My photos ('+photos.length+')']:Lph,['🌐 Wikimedia photos ('+wiki.length+')']:Lwiki,['🖼️ Grand-Tour views ('+redis.length+')']:Lredis,
   ['🏛️ Reconstruction · Greek ('+recon.filter(function(v){return v.period==="greek";}).length+')']:LrecG,
   ['🏛️ Reconstruction · Lucanian ('+recon.filter(function(v){return v.period==="lucanian";}).length+')']:LrecL,
   ['🏛️ Reconstruction · Roman ('+recon.filter(function(v){return v.period==="roman";}).length+')']:LrecR}).addTo(map);
Lredis.addTo(map); LrecG.addTo(map);   // grand-tour + the Greek reconstruction views on by default
map.fitBounds(Lw.getBounds().pad(0.12)); L.control.scale({imperial:false}).addTo(map);
function lbl(lat,lon,t){L.marker([lat,lon],{icon:L.divIcon({className:'',html:'<div class="big">'+t+'</div>',iconSize:[80,16]})}).addTo(map);}
lbl(40.42135,15.00565,'FORUM'); lbl(40.42300,15.00600,'AGORA');
setTimeout(function(){map.invalidateSize();map.fitBounds(Lw.getBounds().pad(0.12));},80);  // legend bar took height from the map
// click any popup image to enlarge (lightbox)
var lb=document.getElementById('lb');
lb.onclick=function(){lb.style.display='none';};
document.addEventListener('click',function(e){
  if(e.target.tagName==='IMG'&&e.target.closest('.leaflet-popup-content')){
    lb.querySelector('img').src=e.target.src;
    var b=e.target.closest('.leaflet-popup-content').querySelector('b');
    lb.querySelector('.cap').textContent=b?b.textContent:'';
    lb.style.display='block'; e.stopPropagation();
  }
});
</script></body></html>'''
html=(T.replace('__WALLS__',json.dumps(fcol(walls))).replace('__GATES__',json.dumps(fcol(gates))).replace('__TOW__',json.dumps(fcol(towers)))
       .replace('__ROADS__',json.dumps(fcol(roads))).replace('__MONS__',json.dumps(fcol(mons))).replace('__PMONS__',json.dumps(fcol(pmons)))
       .replace('__BLD__',json.dumps(fcol(buildings))).replace('__MUS__',json.dumps(fcol(museum))).replace('__ST__',json.dumps(fcol(streets)))
       .replace('__PH__',json.dumps(photos)).replace('__WIKI__',json.dumps(wiki)).replace('__AMPHR__',json.dumps(fcol(amphr))).replace('__REDIS__',json.dumps(redis)).replace('__RECON__',json.dumps(recon)).replace('__COL__',json.dumps(COL)).replace('__PCOL__',json.dumps(PCOL))
       )
open(f"{GIS}/paestum_webmap.html","w").write(html)
print("wrote",f"{GIS}/paestum_webmap.html","(%.1f MB)"%(len(html)/1e6))
