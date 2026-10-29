# /// script
# requires-python = ">=3.14"
# dependencies = ["shapely==2.1.2", "pymupdf==1.26.7"]
# ///
"""Run genuine KiCad checks, compare nets and coordinates, and export/read back CAD.

Default succeeds only when checks are clean. --draft allows specifically reported
unconnected items only; geometric DRC findings always fail in either mode.
The JSON remains an honest count and is NOT a fabrication approval.
"""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, subprocess, xml.etree.ElementTree as ET
from kicad_runtime import configure
configure()
import pcbnew as pcb
from shapely.geometry import box, LineString, Point, Polygon
import pymupdf
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'design/pcb'; R=D/'reports'; E=D/'exports'; NAME='keycult66'
parser=argparse.ArgumentParser();parser.add_argument('--draft',action='store_true');args=parser.parse_args()
R.mkdir(parents=True,exist_ok=True); E.mkdir(parents=True,exist_ok=True)
def run(*args):
 command=['kicad-cli',*map(str,args)];r=subprocess.run(command,check=False,capture_output=True,text=True)
 print(r.stdout.strip())
 if r.returncode:raise RuntimeError(f'{command}: {r.returncode}\n{r.stderr}')
 return command
commands=[]
commands.append(run('sch','erc','--format','json','--severity-all','-o',R/'erc.json',D/(NAME+'.kicad_sch')))
commands.append(run('sch','export','netlist','--format','kicadxml','-o',R/'netlist.xml',D/(NAME+'.kicad_sch')))
commands.append(run('pcb','drc','--schematic-parity','--refill-zones','--save-board','--format','json','--severity-all','-o',R/'drc.json',D/(NAME+'.kicad_pcb')))
b=pcb.LoadBoard(str(D/(NAME+'.kicad_pcb')));fps={f.GetReference():f for f in b.GetFootprints()}; errs=[]
def check(ok,message):
 if not ok:errs.append(message)
def xy(p):return (pcb.ToMM(p.x),pcb.ToMM(p.y))
keys=json.loads((ROOT/'design/preliminary/layout.json').read_text())['preferred']['keys']
circuit=json.loads((D/'circuit.json').read_text());expectedparts={p['ref']:p for p in circuit['parts'] if p['fp']}
check(set(fps)==set(expectedparts),'Schematic/PCB footprint reference set differs')
check(len(keys)==66,'Expected 66 preferred.keys')
coord=[]
for i,k in enumerate(keys,1):
 f=fps[f'SW{i}'];expected=(180+k['x_mm'],100+k['y_mm'])
 # Inspect actual 4mm stem NPTH, not the footprint anchor.
 stem=next(p for p in f.Pads() if not p.GetNumber() and pcb.ToMM(p.GetDrillSize().x)>3.9)
 actual=xy(stem.GetPosition());delta=max(abs(actual[j]-expected[j]) for j in [0,1]);check(delta<.00001,'Stem position '+k['id'])
 check(f.GetValue().startswith(k['id']+' '),'Wrong key ID '+k['id'])
 check(fps[f'D{i}'].GetLayer()==pcb.B_Cu,'Diode not bottom-mounted '+k['id'])
 coord.append({'id':k['id'],'switch':f'SW{i}','expected_stem_mm':expected,'actual_stem_mm':actual,'error_mm':delta})
netroot=ET.parse(R/'netlist.xml').getroot()
schnet={(n.attrib['ref'],n.attrib['pin']):net.attrib['name'].replace('/','{slash}') for net in netroot.find('nets') for n in net.findall('node')}
netdiff=[]
for ref,f in fps.items():
 for p in f.Pads():
  if not p.GetNumber():continue
  key=(ref,p.GetNumber());a=schnet.get(key,'');actual=p.GetNetname()
  if a!=actual:netdiff.append({'ref':ref,'pin':p.GetNumber(),'schematic':a,'pcb':actual})
check(not netdiff,'Actual KiCad netlist and PCB pad net mismatch')
keepout=box(155,75,205,125); bad=[]
for f in fps.values():
 # Courtyard covers body, not potentially offboard reference fields.
 for shape in f.GraphicalItems():
  if shape.GetLayer() in (pcb.F_CrtYd,pcb.B_CrtYd):
   a=shape.GetBoundingBox();g=box(*xy(a.GetOrigin()),*xy(a.GetEnd()))
   if g.intersection(keepout).area>1e-8:bad.append('courtyard:'+f.GetReference())
 for p in f.Pads():
  a=p.GetBoundingBox();g=box(*xy(a.GetOrigin()),*xy(a.GetEnd()))
  if g.intersection(keepout).area>1e-8:bad.append('pad:'+f.GetReference()+':'+p.GetNumber())
for t in b.GetTracks():
 if isinstance(t,pcb.PCB_VIA):g=Point(*xy(t.GetPosition())).buffer(pcb.ToMM(t.GetWidth(pcb.F_Cu))/2)
 else:g=LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(pcb.ToMM(t.GetWidth())/2)
 if g.intersects(keepout):bad.append('copper:'+t.GetNetname())
# Verify the actual board rule area has every restriction on all enabled copper layers.
zones=list(b.Zones());rules=[z for z in zones if z.GetIsRuleArea()]
check(len(rules)==1,'Expected one central rule area')
if rules:
 z=rules[0];check(all([z.GetDoNotAllowTracks(),z.GetDoNotAllowVias(),z.GetDoNotAllowPads(),z.GetDoNotAllowZoneFills(),z.GetDoNotAllowFootprints()]),'Central rule area restriction missing')
 for layer in [pcb.F_Cu,pcb.In1_Cu,pcb.In2_Cu,pcb.B_Cu]:check(z.GetLayerSet().Contains(layer),'Keepout missing copper layer')
# Inspect filled polygons too; outline-with-hole geometry must not occupy the reserve.
for z in zones:
 if z.GetIsRuleArea():continue
 for layer in [pcb.F_Cu,pcb.In1_Cu,pcb.In2_Cu,pcb.B_Cu]:
  if not z.GetLayerSet().Contains(layer):continue
  filled=z.GetFilledPolysList(layer)
  def chain(c):return [xy(c.CPoint(i)) for i in range(c.PointCount())]
  for j in range(filled.OutlineCount()):
   g=Polygon(chain(filled.COutline(j)),[chain(filled.CHole(j,h)) for h in range(filled.HoleCount(j))])
   if g.intersection(keepout).area>1e-8:bad.append('filled-copper:'+z.GetNetname())
check(not bad,'Component/copper intersects central reservation: '+str(sorted(set(bad))))
# A rectangular envelope only: no inner Edge.Cuts and no inherited tray mounting holes.
edges=[x for x in b.GetDrawings() if x.GetLayer()==pcb.Edge_Cuts]
check(len(edges)==4,'Working envelope must have four edges, no invented central cutout')
epts=[xy(p) for e in edges for p in [e.GetStart(),e.GetEnd()]]
bounds=[min(p[0] for p in epts),min(p[1] for p in epts),max(p[0] for p in epts),max(p[1] for p in epts)]
check(all(abs(a-z)<.00001 for a,z in zip(bounds,[37.5,52.7,322.5,147.3])),'GH60 scalar envelope bounds differ from 285.0 x 94.6 mm')
commands.append(run('sch','export','pdf','--exclude-pdf-property-popups','-o',E/'schematic.pdf',D/(NAME+'.kicad_sch')))
commands.append(run('sch','export','svg','-o',str(E/'schematic')+'/',D/(NAME+'.kicad_sch')))
for side,layers in [('front','F.Cu,F.SilkS,Edge.Cuts,Dwgs.User'),('back','B.Cu,B.SilkS,Edge.Cuts,Dwgs.User'),('ground','In1.Cu,Edge.Cuts,Dwgs.User')]:
 commands.append(run('pcb','export','svg','--layers',layers,'--mode-single','--fit-page-to-board','--exclude-drawing-sheet','-o',E/(side+'.svg'),D/(NAME+'.kicad_pcb')))
commands.append(run('pcb','export','pdf','--layers','F.Cu,B.Cu,In1.Cu,In2.Cu,Edge.Cuts,Dwgs.User','--mode-multipage','--scale','0','-o',E/'board-layers.pdf',D/(NAME+'.kicad_pcb')))
readback={}
for p in sorted(E.rglob('*.svg')):
 # Normalize KiCad trailing spaces without changing vector geometry.
 p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')
 root=ET.parse(p).getroot();check(root.tag.endswith('svg'),'SVG parse failure '+str(p));readback[str(p.relative_to(D))]={'bytes':p.stat().st_size,'viewBox':root.attrib.get('viewBox')}
for p in [E/'schematic.pdf',E/'board-layers.pdf']:
 doc=pymupdf.open(p);check(len(doc)>0,'Empty PDF '+str(p));readback[str(p.relative_to(D))]={'pages':len(doc),'page_sizes_pt':[[p.rect.width,p.rect.height] for p in doc]}
 if p.name=='schematic.pdf':
  doc[0].get_pixmap(matrix=pymupdf.Matrix(.9,.9)).save(str(E/'schematic-preview.png'))
  # Native PDF crop for checking fine MCU, power, flash and crystal connections.
  doc[0].get_pixmap(matrix=pymupdf.Matrix(2,2),clip=pymupdf.Rect(15*72/25.4,48*72/25.4,290*72/25.4,190*72/25.4)).save(str(E/'mcu-schematic-detail.png'))
erc=json.loads((R/'erc.json').read_text());drc=json.loads((R/'drc.json').read_text())
eitems=[v for s in erc.get('sheets',[]) for v in s.get('violations',[])];viol=drc['violations'];unconn=drc['unconnected_items'];parity=drc['schematic_parity']
check(not eitems,'ERC violations');check(not parity,'KiCad native schematic parity violations')
summary={'status':('validation failed' if errs or viol else 'reviewable draft; NOT manufacturing approval'),'kicad_version':pcb.GetBuildVersion(),'erc_count':len(eitems),'erc_by_type':dict(Counter(v['type'] for v in eitems)),'drc_count':len(viol),'drc_by_type':dict(Counter(v['type'] for v in viol)),'drc_by_severity':dict(Counter(v['severity'] for v in viol)),'unconnected_item_count':len(unconn),'unconnected_nets':sorted({i['description'].split('[')[1].split(']')[0] for v in unconn for i in v['items'] if '[' in i['description']}),'schematic_parity_count':len(parity),'independent_netlist_mismatch_count':len(netdiff),'envelope_bounds_mm':bounds,'switch_count':66,'diode_count':66,'footprint_count':len(fps),'net_count':len(list(b.GetNetInfo().NetsByNetcode()))-1,'track_segment_count':sum(not isinstance(t,pcb.PCB_VIA) for t in b.GetTracks()),'via_count':sum(isinstance(t,pcb.PCB_VIA) for t in b.GetTracks()),'signal_tracks_on_ground_layer':sum(t.GetLayer()==pcb.In1_Cu and t.GetNetname()!='GND' for t in b.GetTracks() if not isinstance(t,pcb.PCB_VIA)),'keepout_intersections':sorted(set(bad)),'structural_errors':errs,'native_export_readback':readback,'commands':commands,'artifact_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [D/(NAME+ext) for ext in ['.kicad_pro','.kicad_sch','.kicad_pcb']]}}
(R/'validation.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n');(R/'switch-coordinates.json').write_text(json.dumps(coord,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['commands','native_export_readback','artifact_sha256']},indent=2))
if errs or viol or (not args.draft and unconn):raise SystemExit(1)
