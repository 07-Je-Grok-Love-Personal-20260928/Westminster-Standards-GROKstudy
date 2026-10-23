# -*- coding: utf-8 -*-
"""v3.0 geography helpers.
Natural Earth (public domain, naturalearthdata.com) -> (1) small self-hosted GeoJSON base layers for Leaflet
(docs/assets/geo/*.json) and (2) projected SVG paths for the hand-drawn concept maps.
Modern political borders are intentionally NOT drawn (land is dissolved): the maps are about the 16th-17th c."""
import json, os, math, urllib.request
from shapely.geometry import shape, box, mapping, MultiPolygon, Polygon, LineString, MultiLineString
from shapely.ops import unary_union
HERE=os.path.dirname(os.path.abspath(__file__))
RAW=os.environ.get('NE_DIR','/workspace/ne')
NE='https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'
CACHE=os.path.join(HERE,'data','geo_cache.json')
OUTGEO=os.path.join(HERE,'..','docs','assets','geo')
_raw={}
def raw(name):
    if name in _raw: return _raw[name]
    p=os.path.join(RAW,name+'.geojson')
    if not os.path.exists(p):
        os.makedirs(RAW,exist_ok=True); urllib.request.urlretrieve(NE+name+'.geojson',p)
    _raw[name]=json.load(open(p)); return _raw[name]
_land={}
def land(res='50m'):
    if res not in _land:
        _land[res]=unary_union([shape(f['geometry']).buffer(0) for f in raw(f'ne_{res}_admin_0_countries')['features']])
    return _land[res]
def rivers(names=None,maxrank=6):
    out=[]
    for f in raw('ne_50m_rivers_lake_centerlines')['features']:
        p=f['properties']
        if p['scalerank']<=maxrank and (names is None or p.get('name') in names): out.append((p.get('name'),shape(f['geometry'])))
    return out
def lakes():
    return unary_union([shape(f['geometry']) for f in raw('ne_50m_lakes')['features'] if f['properties']['scalerank']<=2])
def _r(c,n): return [round(c[0],n),round(c[1],n)]
def _rc(geom,n):
    g=mapping(geom)
    def rr(x):
        if isinstance(x[0],(int,float)): return _r(x,n)
        return [rr(y) for y in x]
    g['coordinates']=rr(g['coordinates']); return g
def export_layers():
    """write self-hosted base layers; tiny + cached so the build needs no network once cached"""
    os.makedirs(OUTGEO,exist_ok=True)
    cache=json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    if 'eu' not in cache or 'world' not in cache:
        eb=box(-14,33,36,64)
        L=land('50m').intersection(eb).simplify(0.015,preserve_topology=True)
        R=[{'type':'Feature','properties':{'n':n},'geometry':_rc(g.intersection(eb).simplify(0.01),3)} for n,g in rivers(maxrank=6) if g.intersects(eb)]
        R=[f for f in R if f['geometry']['coordinates']]
        K=lakes().intersection(eb).simplify(0.015)
        eu={'type':'FeatureCollection','features':[{'type':'Feature','properties':{'k':'land'},'geometry':_rc(L,3)}]+[dict(f,properties={'k':'river','n':f['properties']['n']}) for f in R]+([{'type':'Feature','properties':{'k':'lake'},'geometry':_rc(K,3)}] if not K.is_empty else [])}
        W=land('110m').simplify(0.08,preserve_topology=True)
        world={'type':'FeatureCollection','features':[{'type':'Feature','properties':{'k':'land'},'geometry':_rc(W,2)}]}
        cache['eu']=eu; cache['world']=world
        json.dump(cache,open(CACHE,'w'),separators=(',',':'))
    for k in ('eu','world'):
        json.dump(cache[k],open(os.path.join(OUTGEO,k+'.json'),'w'),separators=(',',':'))
    return {k:os.path.getsize(os.path.join(OUTGEO,k+'.json')) for k in ('eu','world')}
# ---------------- projection + SVG ----------------
class Proj:
    """equirectangular, x scaled by cos(mid-latitude); bbox=(lon0,lat0,lon1,lat1) -> W x H viewBox"""
    def __init__(s,bbox,W):
        s.b=bbox; lon0,lat0,lon1,lat1=bbox; s.k=math.cos(math.radians((lat0+lat1)/2))
        s.W=W; s.sc=W/((lon1-lon0)*s.k); s.H=round((lat1-lat0)*s.sc)
    def __call__(s,lon,lat):
        return ((lon-s.b[0])*s.k*s.sc, (s.b[3]-lat)*s.sc)
def _ring(coords,P,tol):
    pts=[P(*c) for c in coords]
    ls=LineString(pts).simplify(tol) if len(pts)>3 else LineString(pts)
    xs=list(ls.coords)
    if len(xs)<3: return ''
    return 'M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in xs)+'Z'
def svg_land(bbox,W,res='50m',tol=0.9,minarea=6):
    P=Proj(bbox,W); lon0,lat0,lon1,lat1=bbox
    g=land(res).intersection(box(lon0-1,lat0-1,lon1+1,lat1+1))
    polys=list(g.geoms) if hasattr(g,'geoms') else [g]
    d=[]
    for p in polys:
        if not isinstance(p,Polygon): continue
        # drop specks
        x0,y0=P(p.bounds[0],p.bounds[3]); x1,y1=P(p.bounds[2],p.bounds[1])
        if (x1-x0)*(y1-y0)<minarea: continue
        d.append(_ring(p.exterior.coords,P,tol))
        for i in p.interiors: d.append(_ring(i.coords,P,tol))
    return P,''.join(d)
def svg_rivers(P,names,tol=0.8):
    lon0,lat0,lon1,lat1=P.b; out=[]
    for n,g in rivers(names=names,maxrank=8):
        g=g.intersection(box(lon0,lat0,lon1,lat1))
        ls=list(g.geoms) if hasattr(g,'geoms') else [g]
        for l in ls:
            if l.is_empty or not hasattr(l,'coords'): continue
            pts=list(LineString([P(*c) for c in l.coords]).simplify(tol).coords)
            if len(pts)>1: out.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in pts))
    return ''.join(out)
if __name__=='__main__':
    print(export_layers())
