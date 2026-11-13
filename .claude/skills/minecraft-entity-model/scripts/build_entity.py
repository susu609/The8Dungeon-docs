#!/usr/bin/env python3
"""Build a Minecraft entity (Blockbench modded_entity, box UV) from a JSON spec.
Outputs: <name>.bbmodel, <name>.png (texture), <name>_views.png (4-angle render),
<name>_texture_preview.png. Usage: build_entity.py spec.json OUT_DIR
Texturing follows the Minecraft Style Guide: fixed palette (no blending), one tone
per face by direction (top/front brighter than bottom/back), optional bottom shadow row.
"""
import json, sys, os, io, math, base64, uuid
from PIL import Image, ImageDraw, ImageFilter

def hexc(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))+(255,)

def faces(u,v,w,h,d):
    return {"up":(u+d,v,w,d),"down":(u+d+w,v,w,d),"east":(u,v+d,d,h),"north":(u+d,v+d,w,h),
            "west":(u+d+w,v+d,d,h),"south":(u+d+w+d,v+d,w,h)}

DEFAULT_FACE_TONE={"up":"light","north":"mid","east":"dark","west":"dark","south":"darker","down":"darkest"}

def pack_uv(cubes,T):
    """Shelf-pack box-UV islands when 'uv' is omitted."""
    x=y=row=0
    for c in cubes:
        if "uv" in c: continue
        w,h,d=c["size"]; iw,ih=2*(w+d),h+d
        if x+iw>T: x,y,row=0,y+row,0
        c["uv"]=[x,y]; x+=iw; row=max(row,ih)
        if y+ih>T: sys.exit(f"texture {T}px too small for UVs; raise 'texture_size'")

def build(spec,out):
    T=spec.get("texture_size",64); name=spec["name"]
    pal={k:hexc(v) for k,v in spec["palette"].items()}
    cubes=spec["cubes"]; pack_uv(cubes,T)
    tex=Image.new("RGBA",(T,T),(0,0,0,0)); px=tex.load()
    for c in cubes:
        w,h,d=c["size"]; tones={**DEFAULT_FACE_TONE,**spec.get("face_tones",{}),**c.get("face_tones",{})}
        shadow=c.get("bottom_shadow",spec.get("bottom_shadow",True))
        for f,(x,y,fw,fh) in faces(*c["uv"],w,h,d).items():
            tone=tones[f]
            for i in range(fw):
                for j in range(fh):
                    col=pal[tone]
                    if shadow and f not in("up","down") and j==fh-1 and fh>=3:
                        order=["light","mid","dark","darker","darkest"]
                        col=pal[order[min(len(order)-1,order.index(tone)+1)]] if tone in order else col
                    px[x+i,y+j]=col
    # pixel details painted onto a face of a named cube: [cube, face, x, y, palette_key]
    byname={c["name"]:c for c in cubes}
    for cn,f,dx,dy,key in spec.get("details",[]):
        c=byname[cn]; fx,fy,fw,fh=faces(*c["uv"],*c["size"])[f]
        assert 0<=dx<fw and 0<=dy<fh, f"detail out of face: {cn}.{f} {dx},{dy}"
        px[fx+dx,fy+dy]=pal[key]
    os.makedirs(out,exist_ok=True)
    tex.save(f"{out}/{name}.png"); tex.resize((512,512),Image.NEAREST).save(f"{out}/{name}_texture_preview.png")
    buf=io.BytesIO(); tex.save(buf,"PNG")
    els=[]
    for c in cubes:
        o,s=c["from"],c["size"]
        els.append({"name":c["name"],"uuid":str(uuid.uuid4()),"from":o,"to":[o[i]+s[i] for i in range(3)],
          "origin":c.get("pivot",[o[0]+s[0]/2,o[1]+s[1],o[2]+s[2]/2]),"uv_offset":c["uv"],
          "box_uv":True,"rescale":False,"color":0,"faces":{}})
    groups={}
    for c,e in zip(cubes,els): groups.setdefault(c.get("group","body"),[]).append(e["uuid"])
    outl=[{"name":"root","origin":[0,0,0],"uuid":str(uuid.uuid4()),"children":[
        {"name":g,"origin":spec.get("group_pivots",{}).get(g,[0,0,0]),"uuid":str(uuid.uuid4()),"children":ch}
        for g,ch in groups.items()]}]
    bb={"meta":{"format_version":"4.10","model_format":"modded_entity","box_uv":True},
        "name":name,"model_identifier":name,"modded_entity_version":"1.17",
        "resolution":{"width":T,"height":T},"elements":els,"outliner":outl,
        "textures":[{"name":f"{name}.png","id":"0","width":T,"height":T,"uv_width":T,"uv_height":T,
          "uuid":str(uuid.uuid4()),"source":"data:image/png;base64,"+base64.b64encode(buf.getvalue()).decode()}]}
    json.dump(bb,open(f"{out}/{name}.bbmodel","w"),indent=1)
    render_sheet(cubes,px,f"{out}/{name}_views.png")
    lint(spec,cubes,tex)

def lint(spec,cubes,tex):
    warn=[]
    for c in cubes:
        if any(v<1 or v!=int(v) for v in c["size"]): warn.append(f"mixel: {c['name']} size {c['size']}")
    n=len([c for _,c in (tex.getcolors(4096) or []) if c[3]])
    if n>8: warn.append(f"{n} distinct colours (>8): palette not restricted")
    if len(cubes)>12: warn.append(f"{len(cubes)} elements: try merging (style guide: keep count low)")
    print("lint:", "OK" if not warn else "\n  - "+"\n  - ".join(warn))

def render(cubes,px,yaw,pitch,S=640,ss=3):
    R=S*ss; ys=[c["from"][1]+c["size"][1] for c in cubes]; ext=max(max(abs(v) for c in cubes for v in c["from"]+[c["from"][i]+c["size"][i] for i in range(3)]),max(ys))
    k=R*0.3/ext; cy_=max(ys)/2
    cy,sy,cp,sp=math.cos(yaw),math.sin(yaw),math.cos(pitch),math.sin(pitch)
    def P(x,y,z):
        y-=cy_; x2=x*cy-z*sy; z2=x*sy+z*cy
        return (R/2+x2*k, R/2-(y*cp-z2*sp)*k, y*sp+z2*cp)
    bg=Image.new("RGBA",(R,R),(0,0,0,0)); bd=ImageDraw.Draw(bg); g=int(ext*1.5)
    for t in range(-g,g+1,2):
        bd.line([P(t,0,-g)[:2],P(t,0,g)[:2]],fill=(255,255,255,18),width=ss)
        bd.line([P(-g,0,t)[:2],P(g,0,t)[:2]],fill=(255,255,255,18),width=ss)
    sh=Image.new("RGBA",(R,R),(0,0,0,0))
    ImageDraw.Draw(sh).polygon([P(ext*1.1*math.cos(a),0,ext*0.7*math.sin(a))[:2] for a in [i*math.pi/18 for i in range(36)]],fill=(0,0,0,120))
    bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6*ss)))
    img=Image.new("RGBA",(R,R),(0,0,0,0)); dr=ImageDraw.Draw(img); polys=[]
    for c in cubes:
        (x0,y0,z0),(w,h,d)=c["from"],c["size"]; x1,y1,z1=x0+w,y0+h,z0+d
        F=faces(*c["uv"],w,h,d)
        defs={"north":((x1,y1,z0),(-1,0,0),(0,-1,0),(0,0,-1)),"south":((x0,y1,z1),(1,0,0),(0,-1,0),(0,0,1)),
              "east":((x1,y1,z1),(0,0,-1),(0,-1,0),(1,0,0)),"west":((x0,y1,z0),(0,0,1),(0,-1,0),(-1,0,0)),
              "up":((x1,y1,z1),(-1,0,0),(0,0,-1),(0,1,0)),"down":((x1,y0,z0),(-1,0,0),(0,0,1),(0,-1,0))}
        for f,(org,ua,va,(nx,ny,nz)) in defs.items():
            if ny*sp+(nx*sy+nz*cy)*cp>=0: continue
            tx,ty,tw,th=F[f]
            for i in range(tw):
                for j in range(th):
                    col=px[tx+i,ty+j]
                    if col[3]==0: continue
                    pts=[P(*(org[q]+ua[q]*a+va[q]*b for q in range(3))) for a,b in((i,j),(i+1,j),(i+1,j+1),(i,j+1))]
                    polys.append((sum(p[2] for p in pts)/4,[p[:2] for p in pts],col[:3]))
    polys.sort(key=lambda t:-t[0])
    for _,pts,col in polys: dr.polygon(pts,fill=col,outline=col)
    edge=Image.new("RGBA",(R,R),(40,20,14,255)); edge.putalpha(img.split()[3].filter(ImageFilter.MaxFilter(2*ss+1)))
    bg.alpha_composite(edge); bg.alpha_composite(img)
    return bg.resize((S,S),Image.LANCZOS)

def render_sheet(cubes,px,path):
    views=[("FRONT",0.0,-0.08),("3/4",0.65,-0.42),("SIDE",-math.pi/2,-0.08),("BACK 3/4",math.pi-0.7,-0.42)]
    S=640; W=S*len(views); sheet=Image.new("RGBA",(W,S+40)); d=ImageDraw.Draw(sheet)
    for y in range(S+40):
        t=y/(S+40); d.line([(0,y),(W,y)],fill=(int(52-26*t),int(56-28*t),int(68-32*t)))
    for i,(t,yw,pt) in enumerate(views):
        sheet.alpha_composite(render(cubes,px,yw,pt,S),(i*S,40)); d.text((i*S+24,18),t,fill=(235,225,215))
    sheet.save(path)

if __name__=="__main__":
    if len(sys.argv)!=3: sys.exit(__doc__)
    build(json.load(open(sys.argv[1])),sys.argv[2])
