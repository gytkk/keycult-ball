# /// script
# requires-python = ">=3.11"
# dependencies = ["sexpdata==1.0.2"]
# ///
"""Remove KiCad-reported dead-end copper; never suppress DRC or unconnected nets.

Use maintained sexpdata for these small native-file edits. KiCad 10's installed
SWIG deletion bindings proved unstable; all geometry is reloaded and checked by
kicad-cli after every edit. Refill first so real ground-plane vias are retained.
"""
from pathlib import Path
import json,subprocess,uuid
import sexpdata as sx
ROOT=Path(__file__).resolve().parents[1];FP=ROOT/'design/pcb/keycult66.kicad_pcb';REPORT=ROOT/'.cache/pcb-tools/cleanup-drc.json'
S=sx.Symbol
def tag(x,name):return isinstance(x,list) and x and str(x[0])==name
def child(x,name):return next((a for a in x if tag(a,name)),None)
def save(a):FP.write_text(sx.dumps(a)+'\n')
a=sx.load(FP.open());vias=[x for x in a if tag(x,'via')];pair=[]
for v in vias:
 x,y=child(v,'at')[1:3]
 if abs(x-184.388)<.002 and (abs(y-67.2)<.002 or abs(y-67.6)<.002):pair.append(v)
if len(pair)==2 and child(pair[0],'net')==child(pair[1],'net'):
 pair.sort(key=lambda x:child(x,'at')[2]);start=child(pair[0],'at')[1:];end=child(pair[1],'at')[1:];net=child(pair[1],'net');a.remove(pair[0])
 for layer in ('F.Cu','B.Cu'):
  a.append([S('segment'),[S('start'),*start],[S('end'),*end],[S('width'),.15],[S('layer'),layer],net,[S('uuid'),str(uuid.uuid5(uuid.NAMESPACE_URL,'keycult66-same-net-via-bridge-'+layer))]])
 save(a)
removed=[]
for _ in range(12):
 subprocess.run(['kicad-cli','pcb','drc','--refill-zones','--save-board','--format','json','-o',str(REPORT),str(FP)],check=True,stdout=subprocess.DEVNULL)
 report=json.loads(REPORT.read_text());dead=[v for v in report['violations'] if v['type'] in ('track_dangling','via_dangling')]
 if not dead:break
 ids={i['uuid'] for v in dead for i in v['items']};a=sx.load(FP.open());new=[]
 for n in a:
  u=child(n,'uuid') if isinstance(n,list) else None
  if (tag(n,'segment') or tag(n,'via')) and u and u[1] in ids:removed.append(u[1])
  else:new.append(n)
 save(new)
else:raise RuntimeError('Dead-end cleanup did not converge; inspect actual DRC')
print('Removed',len(removed),'KiCad-confirmed open-ended tracks/vias. Rules and unconnected reports unchanged.')
