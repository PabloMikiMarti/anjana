import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
animdir, modname, scene_name, out = sys.argv[1:5]
os.environ['MINI_OUT']=out
sys.path.insert(0, animdir)
mod=importlib.import_module(modname)
S=getattr(mod,scene_name)(); S.construct(); S.close()
print(scene_name, os.environ.get('THEME'), f'{S.t:.1f}s', S.nframes, 'frames')
