#!/usr/bin/env python3
"""Rebuild the editable Base underlays and optional matching PNG previews."""
from pathlib import Path
import argparse
import json
import shlex
import subprocess
from concurrent.futures import ThreadPoolExecutor
from build_view_templates import build_all as views
from build_surface_templates import build_all as surfaces
from build_admin_templates import build_all as admin
from build_companion_templates import build_all as companions
from build_mobile_templates import build_all as mobile

HERE=Path(__file__).resolve().parent
REFERENCE_IDS=['desktop-grid','kanban','calendar','gantt','gallery','form-edit','form-fill','dashboard','questionnaire','questionnaire-results','workflow','advanced-permissions']

def build(render=False,renderer=None):
    boards=views()+surfaces()+admin()+companions()+mobile()
    by_id={b.key:b for b in boards}
    ordered=[by_id[k] for k in REFERENCE_IDS]+[b for b in boards if b.key not in REFERENCE_IDS]
    for b in ordered:
        b.meta['reference']={'kind':'screenshot-layout-redraw','reference_index':REFERENCE_IDS.index(b.key)+1} if b.key in REFERENCE_IDS else {'kind':'companion-template','scope':'示意模板，具体面板以用户最新参考为准'}
        b.write()
    catalog={'schema_version':2,'layout_revision':'minimal-background-v3','aliases':{'form':'form-fill','app-dashboard':'dashboard'},'templates':[b.meta for b in ordered]}
    (HERE/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    for name in ('form.svg','form.png','app-dashboard.svg','app-dashboard.png'):
        (HERE/name).unlink(missing_ok=True)
    if render:
        command=shlex.split(renderer) if renderer else ['npx','-y','@larksuite/whiteboard-cli@0.2.13']
        def one(b):
            subprocess.run(command+['-f','svg','--scale','1','-i',str(HERE/b.meta['svg']),'-o',str(HERE/b.meta['png'])],check=True,stdout=subprocess.DEVNULL)
        with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(one,ordered))
    return ordered

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--render',action='store_true')
    p.add_argument('--renderer',help='Optional executable or quoted command for whiteboard-cli')
    args=p.parse_args()
    build(args.render,args.renderer)
