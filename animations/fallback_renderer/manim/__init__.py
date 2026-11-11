"""mini-manim: a small renderer for the subset of Manim used by the Anjana scenes.
Same layout rules as Manim (Cairo renderer); text from the real TTFs via FreeType."""
import numpy as np, os, copy as _copy, math, subprocess
from PIL import Image, ImageDraw, ImageFont

UP=np.array([0.,1,0]);DOWN=-UP;RIGHT=np.array([1.,0,0]);LEFT=-RIGHT;ORIGIN=np.zeros(3);OUT=np.array([0,0,1.])
UL=UP+LEFT;UR=UP+RIGHT;DL=DOWN+LEFT;DR=DOWN+RIGHT
PI=np.pi;TAU=2*np.pi;NORMAL='NORMAL';ITALIC='ITALIC';MEDIUM='MEDIUM';BOLD='BOLD';SEMIBOLD='SEMIBOLD'
class _C: pass
config=_C(); config.background_color='#000000'; config.pixel_width=1920; config.pixel_height=1080; config.frame_rate=24
config.frame_width=14.222222222222221; config.frame_height=8.0
def _sig(x): return 1/(1+math.exp(-x))
def smooth(t, inflection=10.0):
    e=_sig(-inflection/2); return min(max((_sig(inflection*(t-0.5))-e)/(1-2*e),0),1)
def linear(t): return t
def there_and_back(t, inflection=10.0): return smooth(2*t if t<0.5 else 2*(1-t), inflection)
def double_smooth(t): return 0.5*smooth(2*t) if t<0.5 else 0.5*(1+smooth(2*t-1))
class _RF:
    @staticmethod
    def ease_in_out_cubic(t): return 4*t**3 if t<0.5 else 1-(-2*t+2)**3/2
    smooth=staticmethod(smooth); linear=staticmethod(linear); there_and_back=staticmethod(there_and_back)
rate_functions=_RF()
DEFAULT_STROKE_WIDTH=4
FONTDIR=os.environ['MINI_FONTDIR']; K=0.0139
_fonts={}
def _fontfile(name, weight):
    if name.startswith('SdM'): return 'SdMManim-Regular.ttf'
    if 'Newsreader' in name: return 'newsreader-400-normal.ttf'
    return {'MEDIUM':'ibm-plex-sans-500-normal.ttf','SEMIBOLD':'ibm-plex-sans-600-normal.ttf','BOLD':'ibm-plex-sans-600-normal.ttf'}.get(weight,'ibm-plex-sans-400-normal.ttf')
def _font(fn, size):
    k=(fn, size)
    if k not in _fonts: _fonts[k]=ImageFont.truetype(os.path.join(FONTDIR,fn), size)
    return _fonts[k]
def _rgb(c):
    if c is None: return None
    if isinstance(c,(tuple,list,np.ndarray)): return np.array(c[:3],float)
    c=c.lstrip('#'); return np.array([int(c[i:i+2],16) for i in (0,2,4)],float)

class Mobject:
    def __init__(self, pts=None, color=None, stroke_color=None, fill_color=None, stroke_width=None,
                 fill_opacity=None, stroke_opacity=1.0, closed=False, **kw):
        self.submobjects=[]; self.pts=np.zeros((0,3)) if pts is None else np.array(pts,float).reshape(-1,3)
        base = color if color is not None else '#FFFFFF'
        self.stroke=_rgb(stroke_color if stroke_color is not None else base)
        self.fill=_rgb(fill_color if fill_color is not None else base)
        self.sw = DEFAULT_STROKE_WIDTH if stroke_width is None else stroke_width
        self.fo = 0.0 if fill_opacity is None else fill_opacity
        self.so = stroke_opacity
        self.closed=closed; self.om=1.0; self.partial=1.0; self.kind=type(self).__name__
    def add(self,*m):
        for x in m:
            if x is not None and x not in self.submobjects: self.submobjects.append(x)
        return self
    def remove(self,*m): self.submobjects=[x for x in self.submobjects if x not in m]; return self
    def family(self):
        out=[self]
        for s in self.submobjects: out+=s.family()
        return out
    def all_points(self):
        ps=[m.pts for m in self.family() if len(m.pts)]
        return np.vstack(ps) if ps else np.zeros((1,3))
    def __getitem__(self,i):
        r=self.submobjects[i]
        return VGroup(*r) if isinstance(i,slice) else r
    def __len__(self): return len(self.submobjects)
    def __iter__(self): return iter(list(self.submobjects))
    def copy(self): return _copy.deepcopy(self)
    def _bb(self): p=self.all_points(); return p.min(0),p.max(0)
    def get_critical_point(self,d):
        lo,hi=self._bb(); c=(lo+hi)/2; r=c.copy()
        for i in (0,1):
            if d[i]>0: r[i]=hi[i]
            elif d[i]<0: r[i]=lo[i]
        return r
    def get_center(self): return self.get_critical_point(ORIGIN)
    def get_left(self): return self.get_critical_point(LEFT)
    def get_right(self): return self.get_critical_point(RIGHT)
    def get_top(self): return self.get_critical_point(UP)
    def get_bottom(self): return self.get_critical_point(DOWN)
    def get_corner(self,d): return self.get_critical_point(d)
    def get_x(self): return self.get_center()[0]
    def get_y(self): return self.get_center()[1]
    @property
    def width(self): lo,hi=self._bb(); return hi[0]-lo[0]
    @property
    def height(self): lo,hi=self._bb(); return hi[1]-lo[1]
    def shift(self,*v):
        v=sum(np.array(x,float) for x in v)
        for m in self.family(): m.pts=m.pts+v
        return self
    def move_to(self,p,aligned_edge=ORIGIN,coor_mask=np.array([1,1,1])):
        target=p.get_critical_point(aligned_edge) if isinstance(p,Mobject) else np.array(p,float)
        return self.shift((target-self.get_critical_point(aligned_edge))*coor_mask)
    def set_x(self,x): return self.shift([x-self.get_x(),0,0])
    def set_y(self,y): return self.shift([0,y-self.get_y(),0])
    def next_to(self,o,direction=RIGHT,buff=0.25,aligned_edge=ORIGIN,**kw):
        direction=np.array(direction,float)
        tgt=(o.get_critical_point(aligned_edge+direction) if isinstance(o,Mobject) else np.array(o,float))
        me=self.get_critical_point(aligned_edge-direction)
        return self.shift(tgt+direction*buff-me)
    def align_to(self,o,direction):
        tp=o.get_critical_point(direction) if isinstance(o,Mobject) else np.array(o,float)
        me=self.get_critical_point(direction); d=np.zeros(3)
        for i in (0,1):
            if direction[i]!=0: d[i]=tp[i]-me[i]
        return self.shift(d)
    def to_corner(self,c=UL,buff=0.5):
        w,h=config.frame_width/2,config.frame_height/2
        tgt=np.array([c[0]*(w-buff),c[1]*(h-buff),0]); return self.shift(tgt-self.get_critical_point(c))
    def to_edge(self,e,buff=0.5): return self.to_corner(e,buff)
    def scale(self,f,about_point=None,about_edge=None,**kw):
        if about_point is None: about_point=self.get_critical_point(about_edge) if about_edge is not None else self.get_center()
        c=np.array(about_point,float)
        for m in self.family(): m.pts=c+(m.pts-c)*f
        return self
    def scale_to_fit_width(self,w): return self.scale(w/self.width) if self.width>0 else self
    def scale_to_fit_height(self,h): return self.scale(h/self.height) if self.height>0 else self
    def stretch(self,f,dim):
        c=self.get_center()
        for m in self.family(): m.pts[:,dim]=c[dim]+(m.pts[:,dim]-c[dim])*f
        return self
    def rotate(self,a,about_point=None,**kw):
        c=self.get_center() if about_point is None else np.array(about_point); R=np.array([[np.cos(a),-np.sin(a),0],[np.sin(a),np.cos(a),0],[0,0,1]])
        for m in self.family(): m.pts=c+(m.pts-c)@R.T
        return self
    def arrange(self,direction=RIGHT,buff=0.25,aligned_edge=ORIGIN,center=True,**kw):
        for a,b in zip(self.submobjects,self.submobjects[1:]): b.next_to(a,direction,buff,aligned_edge)
        if center: self.move_to(ORIGIN)
        return self
    def arrange_in_grid(self,rows=None,cols=None,buff=0.25,**kw):
        cols=cols or int(np.ceil(len(self)/rows)); w=max(m.width for m in self)+buff; h=max(m.height for m in self)+buff
        c=self.get_center()
        for i,m in enumerate(self): r,cc=divmod(i,cols); m.move_to([cc*w,-r*h,0])
        return self.move_to(c)
    def set_color(self,c=None,**kw):
        for m in self.family(): m.stroke=_rgb(c); m.fill=_rgb(c)
        return self
    def set_fill(self,color=None,opacity=None,**kw):
        for m in self.family():
            if color is not None: m.fill=_rgb(color)
            if opacity is not None: m.fo=opacity
        return self
    def set_stroke(self,color=None,width=None,opacity=None,**kw):
        for m in self.family():
            if color is not None: m.stroke=_rgb(color)
            if width is not None: m.sw=width
            if opacity is not None: m.so=opacity
        return self
    def set_opacity(self,o):
        for m in self.family(): m.fo=o; m.so=o
        return self
    def set_points_as_corners(self,pts): self.pts=np.array(pts,float).reshape(-1,3); return self
    def get_start(self): return self.pts[0].copy()
    def get_end(self): return self.pts[-1].copy()
    def point_from_proportion(self,a):
        p=self.pts; seg=np.linalg.norm(np.diff(p,axis=0),axis=1); L=seg.sum()
        if L==0: return p[0].copy()
        d=a*L; acc=0
        for i,s in enumerate(seg):
            if acc+s>=d: return p[i]+(p[i+1]-p[i])*((d-acc)/s if s else 0)
            acc+=s
        return p[-1].copy()
    @property
    def animate(self): return _Anim(self)
class _Anim:
    def __init__(self,m): self.__dict__['m']=m; self.__dict__['target']=_copy.deepcopy(m)
    def __getattr__(self,n):
        f=getattr(self.target,n)
        def g(*a,**k): f(*a,**k); return self
        return g
VMobject=Mobject
class VGroup(Mobject):
    def __init__(self,*m,**kw): super().__init__(); self.add(*m)
Group=VGroup
def _circ(r,c=ORIGIN,n=72,a0=0,a1=TAU,end=False): return [np.array(c,float)+[r*np.cos(t),r*np.sin(t),0] for t in np.linspace(a0,a1,n,endpoint=end)]
class Circle(Mobject):
    def __init__(self,radius=1.0,color='#FC6255',**kw): super().__init__(_circ(radius),color=color,closed=True,**kw)
class Dot(Mobject):
    def __init__(self,point=ORIGIN,radius=0.08,color='#FFFFFF',fill_opacity=1.0,stroke_width=0,**kw):
        super().__init__(_circ(radius,point,32),color=color,fill_opacity=fill_opacity,stroke_width=stroke_width,closed=True,**kw)
class Ellipse(Mobject):
    def __init__(self,width=2,height=1,**kw): super().__init__([[width/2*np.cos(t),height/2*np.sin(t),0] for t in np.linspace(0,TAU,72,endpoint=False)],closed=True,**kw)
class Arc(Mobject):
    def __init__(self,radius=1.0,start_angle=0,angle=PI/2,**kw): super().__init__(_circ(radius,ORIGIN,40,start_angle,start_angle+angle,True),**kw)
def _rrect(w,h,r):
    if r<=0: return [[-w/2,-h/2,0],[w/2,-h/2,0],[w/2,h/2,0],[-w/2,h/2,0]]
    pts=[]
    for cx,cy,a0 in ((w/2-r,-h/2+r,-PI/2),(w/2-r,h/2-r,0),(-w/2+r,h/2-r,PI/2),(-w/2+r,-h/2+r,PI)):
        pts+=[[cx+r*np.cos(t),cy+r*np.sin(t),0] for t in np.linspace(a0,a0+PI/2,8)]
    return pts
class Rectangle(Mobject):
    def __init__(self,width=4.0,height=2.0,color='#FFFFFF',_r=0,**kw): super().__init__(_rrect(width,height,_r),color=color,closed=True,**kw)
class RoundedRectangle(Rectangle):
    def __init__(self,corner_radius=0.5,**kw): super().__init__(_r=corner_radius,**kw)
class Square(Rectangle):
    def __init__(self,side_length=2.0,**kw): super().__init__(width=side_length,height=side_length,**kw)
class Polygon(Mobject):
    def __init__(self,*pts,color='#58C4DD',**kw): super().__init__(pts,color=color,closed=True,**kw)
class Line(Mobject):
    def __init__(self,start=LEFT,end=RIGHT,buff=0,color='#FFFFFF',**kw):
        s,e=np.array(start,float),np.array(end,float); d=e-s; L=np.linalg.norm(d)
        if L>0 and buff: s,e=s+d/L*buff,e-d/L*buff
        super().__init__([s,e],color=color,**kw)
class DashedLine(Line): pass
class _Tip(Mobject): pass
class Arrow(Line):
    def __init__(self,start=LEFT,end=RIGHT,buff=0.25,tip_length=0.35,max_tip_length_to_length_ratio=0.25,color='#FFFFFF',stroke_width=6,**kw):
        super().__init__(start,end,buff=buff,color=color,stroke_width=stroke_width,**kw)
        s,e=self.pts[0],self.pts[1]; d=e-s; L=np.linalg.norm(d); u=d/L if L else RIGHT
        tl=min(tip_length,max_tip_length_to_length_ratio*L); n=np.array([-u[1],u[0],0])
        base=e-u*tl
        tip=_Tip([e,base+n*tl/2,base-n*tl/2],color=color,fill_opacity=1,stroke_width=0,closed=True)
        self.pts=np.array([s,base+u*0.001]); self.add(tip)
class SurroundingRectangle(RoundedRectangle):
    def __init__(self,m,buff=0.1,corner_radius=0,color='#FFFF00',**kw):
        super().__init__(width=m.width+2*buff,height=m.height+2*buff,corner_radius=corner_radius,color=color,**kw); self.move_to(m)
class Glyph(Mobject): pass
class Text(Mobject):
    def __init__(self,text,font='',font_size=48,color='#FFFFFF',weight='NORMAL',slant='NORMAL',**kw):
        super().__init__(color=color,fill_opacity=1.0,stroke_width=0); self.text=text
        fn=_fontfile(font,weight); f=_font(fn,1000); em=K*font_size; s=em/1000.0
        lines=text.split('\n'); y=0.0
        for li,line in enumerate(lines):
            for i,ch in enumerate(line):
                if ch.isspace(): continue
                adv=f.getlength(line[:i]) if i else 0
                l,t,r,b=f.getbbox(ch,anchor='ls')
                if r-l<=0 or b-t<=0: continue
                g=Glyph([[(adv+l)*s,-b*s+y,0],[(adv+r)*s,-t*s+y,0]],color=color,fill_opacity=1.0,stroke_width=0)
                g.ch=ch; g.fn=fn; g.l,g.t,g.r,g.b=l,t,r,b; g.h0=(b-t)*s; g.em0=em
                self.add(g)
            y-=em*1.2
        self.move_to(ORIGIN)
MarkupText=Text

# ---------------- animations ----------------
def _state(m): return [(x.pts.copy(),x.stroke.copy(),x.fill.copy(),x.sw,x.fo,x.so,x.om,x.partial) for x in m.family()]
def _setstate(m,st):
    for x,(p,sc,fc,sw,fo,so,om,pa) in zip(m.family(),st): x.pts=p.copy();x.stroke=sc.copy();x.fill=fc.copy();x.sw=sw;x.fo=fo;x.so=so;x.om=om;x.partial=pa
def _interp(a,b,t):
    out=[]
    for (p1,s1,f1,w1,fo1,so1,o1,pa1),(p2,s2,f2,w2,fo2,so2,o2,pa2) in zip(a,b):
        L=lambda u,v:u+(v-u)*t
        out.append((L(p1,p2) if p1.shape==p2.shape else p2, L(s1,s2),L(f1,f2),L(w1,w2),L(fo1,fo2),L(so1,so2),L(o1,o2),L(pa1,pa2)))
    return out
class Animation:
    introducer=False; remover=False
    def __init__(self,mobject=None,run_time=1.0,rate_func=smooth,**kw):
        self.mobject=mobject; self.run_time=run_time; self.rate_func=rate_func; self.kw=kw
    def begin(self,scene):
        if self.introducer: scene.add(self.mobject)
        self.end=_state(self.mobject); self.start=self.make_start()
        _setstate(self.mobject,self.start)
    def make_start(self): return self.end
    def interpolate(self,a): _setstate(self.mobject,_interp(self.start,self.end,self.rate_func(a)))
    def finish(self,scene):
        self.interpolate(1.0)
        if self.remover: scene.remove(self.mobject)
class _Morph(Animation):
    def __init__(self,proxy,**kw): super().__init__(proxy.m,**kw); self.target=proxy.target
    def begin(self,scene): self.start=_state(self.mobject); self.end=_state(self.target)
class FadeIn(Animation):
    introducer=True
    def __init__(self,*mobs,shift=None,scale=1,**kw):
        super().__init__(mobs[0] if len(mobs)==1 else VGroup(*mobs),**kw); self.sh=shift; self.sc=scale
    def make_start(self):
        c=_copy.deepcopy(self.mobject)
        if self.sc!=1: c.scale(self.sc)
        if self.sh is not None: c.shift(-np.array(self.sh,float))
        for x in c.family(): x.om=0.0
        return _state(c)
class FadeOut(FadeIn):
    introducer=False; remover=True
    def begin(self,scene):
        self.start=_state(self.mobject); c=_copy.deepcopy(self.mobject)
        if self.sc!=1: c.scale(self.sc)
        if self.sh is not None: c.shift(np.array(self.sh,float))
        for x in c.family(): x.om=0.0
        self.end=_state(c)
    def finish(self,scene):
        self.interpolate(1.0); scene.remove(self.mobject); _setstate(self.mobject,self.start)
class Create(Animation):
    introducer=True
    def make_start(self):
        c=_copy.deepcopy(self.mobject)
        for x in c.family(): x.partial=0.0
        return _state(c)
Write=DrawBorderThenFill=Create
class GrowFromEdge(Animation):
    introducer=True
    def __init__(self,m,edge,**kw): super().__init__(m,**kw); self.edge=edge
    def make_start(self):
        c=_copy.deepcopy(self.mobject); c.scale(0.0001,about_point=self.mobject.get_critical_point(self.edge)); return _state(c)
class GrowFromCenter(Animation):
    introducer=True
    def make_start(self):
        c=_copy.deepcopy(self.mobject); c.scale(0.0001); return _state(c)
class MoveAlongPath(Animation):
    def __init__(self,m,path,**kw): super().__init__(m,**kw); self.path=path
    def begin(self,scene): pass
    def interpolate(self,a): self.mobject.move_to(self.path.point_from_proportion(self.rate_func(a)))
    def finish(self,scene): self.interpolate(1.0)
class Wait(Animation):
    def begin(self,scene): pass
    def interpolate(self,a): pass
    def finish(self,scene): pass
class AnimationGroup(Animation):
    def __init__(self,*anims,lag_ratio=0.0,run_time=None,rate_func=linear,**kw):
        self.anims=[_as_anim(a) for a in anims]; self.lag_ratio=lag_ratio; self.rate_func=rate_func
        n=len(self.anims); self._rt=run_time
        self.run_time=run_time if run_time is not None else (max(a.run_time for a in self.anims) if self.anims else 0)
    def begin(self,scene):
        n=len(self.anims); T=self.run_time; r=self.lag_ratio
        d=T/((n-1)*r+1) if n else T
        self.times=[(i*r*d, i*r*d+d) for i in range(n)]
        self.started=[False]*n; self.scene=scene
    def interpolate(self,a):
        t=self.rate_func(a)*self.run_time
        for i,(an,(s,e)) in enumerate(zip(self.anims,self.times)):
            if t>=s and not self.started[i]: an.begin(self.scene); self.started[i]=True
            if self.started[i]: an.interpolate(min(max((t-s)/(e-s) if e>s else 1,0),1))
    def finish(self,scene):
        for i,an in enumerate(self.anims):
            if not self.started[i]: an.begin(scene); self.started[i]=True
            an.finish(scene)
class LaggedStart(AnimationGroup):
    def __init__(self,*anims,lag_ratio=0.05,**kw): super().__init__(*anims,lag_ratio=lag_ratio,**kw)
Succession=AnimationGroup
def _as_anim(a): return _Morph(a) if isinstance(a,_Anim) else a

# ---------------- scene + renderer ----------------
SS=int(os.environ.get('MINI_SS','2'))
class Scene:
    def __init__(self):
        self.mobjects=[]; self.t=0.0
        self.W,self.H=config.pixel_width,config.pixel_height; self.fps=config.frame_rate
        self.pxu=self.W/config.frame_width
        self.bg=tuple(int(v) for v in _rgb(config.background_color))
        self.out=os.environ.get('MINI_OUT'); self.proc=None; self.nframes=0
    def add(self,*m):
        for x in m:
            if x in self.mobjects: self.mobjects.remove(x)
            self.mobjects.append(x)
    def remove(self,*m):
        fam=set(id(f) for x in m for f in x.family())
        self.mobjects=[x for x in self.mobjects if id(x) not in fam]
    def play(self,*anims,run_time=None,rate_func=None,**kw):
        anims=[_as_anim(a) for a in anims]
        for a in anims:
            if run_time is not None: a.run_time=run_time
            if rate_func is not None: a.rate_func=rate_func
        T=max(a.run_time for a in anims)
        for a in anims: a.begin(self)
        n=max(1,int(round(T*self.fps)))
        for k in range(n):
            t=k/n*T
            for a in anims: a.interpolate(min(t/a.run_time,1.0) if a.run_time else 1.0)
            self.frame()
        for a in anims: a.finish(self)
        self.t+=T
    def wait(self,t=1.0):
        n=max(1,int(round(t*self.fps)))
        for _ in range(n): self.frame()
        self.t+=t
    # rendering
    def px(self,p): return (self.W*SS/2+p[0]*self.pxu*SS, self.H*SS/2-p[1]*self.pxu*SS)
    def frame(self):
        self.nframes+=1
        if not self.out: return
        im=Image.new('RGB',(self.W*SS,self.H*SS),self.bg); d=ImageDraw.Draw(im,'RGBA')
        seen=set()
        for m in self.mobjects:
            for x in m.family():
                if id(x) in seen: continue
                seen.add(id(x)); self.draw(d,x)
        im=im.resize((self.W,self.H),Image.LANCZOS)
        if self.proc is None:
            self.proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{self.W}x{self.H}',
                '-r',str(self.fps),'-i','-','-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p',self.out],stdin=subprocess.PIPE)
        self.proc.stdin.write(im.tobytes())
    def close(self):
        if self.proc: self.proc.stdin.close(); self.proc.wait()
    def draw(self,d,x):
        if len(x.pts)==0 or x.om<=0.002: return
        if isinstance(x,Glyph):
            if x.fo*x.om<=0.002: return
            lo,hi=x.pts.min(0),x.pts.max(0); h=hi[1]-lo[1]
            if h<=1e-6: return
            em=x.em0*h/x.h0; u=em/1000.0
            size=max(1,round(em*self.pxu*SS*4)/4)
            col=tuple(int(v) for v in x.fill)+(int(255*x.fo*x.om),)
            d.text(self.px([lo[0]-x.l*u, lo[1]+x.b*u]), x.ch, font=_font(x.fn,size), fill=col, anchor='ls')
            return
        pts=x.pts
        if x.partial<0.999:
            if x.partial<=0.001: return
            if isinstance(x,_Tip):
                a=x.partial; 
                if a<0.85: return
            else:
                P=np.vstack([pts,pts[:1]]) if x.closed else pts
                seg=np.linalg.norm(np.diff(P,axis=0),axis=1); L=seg.sum(); dd=x.partial*L; acc=0; out=[P[0]]
                for i,s in enumerate(seg):
                    if acc+s>=dd: out.append(P[i]+(P[i+1]-P[i])*((dd-acc)/s if s else 0)); break
                    out.append(P[i+1]); acc+=s
                pts=np.array(out)
                if x.fo>0 and x.closed:
                    poly=[self.px(p) for p in x.pts]
                    d.polygon(poly, fill=tuple(int(v) for v in x.fill)+(int(255*x.fo*x.om*x.partial),))
                if x.sw>0 and x.so>0:
                    d.line([self.px(p) for p in pts], fill=tuple(int(v) for v in x.stroke)+(int(255*x.so*x.om),), width=max(1,round(x.sw*0.01*self.pxu*SS)), joint='curve')
                return
        poly=[self.px(p) for p in pts]
        if x.fo>0 and x.closed and len(poly)>=3:
            d.polygon(poly, fill=tuple(int(v) for v in x.fill)+(int(255*x.fo*x.om),))
        if x.sw>0 and x.so>0 and len(poly)>=2:
            w=max(1,round(x.sw*0.01*self.pxu*SS))
            line=poly+[poly[0]] if x.closed else poly
            d.line(line, fill=tuple(int(v) for v in x.stroke)+(int(255*x.so*x.om),), width=w, joint='curve')
