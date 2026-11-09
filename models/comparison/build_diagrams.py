"""Build editable BPMN + matching SVG/PNG previews from reviewed model definitions.
Run with Python packages lxml and cairosvg. Schemas, when present, live in /tmp/cooxupe-bpmn-xsd.
These non-executable comparison proposals do not overwrite the group originals.
"""
import json
import math
import textwrap
from collections import Counter
from html import escape
from pathlib import Path
from lxml import etree as E
import cairosvg

ROOT = Path(__file__).resolve().parent
NS = {'bpmn':'http://www.omg.org/spec/BPMN/20100524/MODEL',
      'bpmndi':'http://www.omg.org/spec/BPMN/20100524/DI',
      'dc':'http://www.omg.org/spec/DD/20100524/DC',
      'di':'http://www.omg.org/spec/DD/20100524/DI',
      'xsi':'http://www.w3.org/2001/XMLSchema-instance'}

def el(parent, tag, **attrs):
    prefix, name = tag.split(':')
    return E.SubElement(parent, '{'+NS[prefix]+'}'+name, {k:str(v) for k,v in attrs.items()})

def text(parent, tag, value, **attrs):
    e=el(parent, tag, **attrs);e.text=str(value);return e

def rect(o):return o['x'],o['y'],o['w'],o['h']
def center(o):return o['x']+o['w']/2,o['y']+o['h']/2

def route(a,b):
    ax,ay=center(a);bx,by=center(b)
    if abs(ay-by)<4:
        return [(a['x']+a['w'] if bx>ax else a['x'],ay),(b['x'] if bx>ax else b['x']+b['w'],by)]
    if abs(ax-bx)<4:
        return [(ax,a['y']+a['h'] if by>ay else a['y']),(bx,b['y'] if by>ay else b['y']+b['h'])]
    if bx>=ax:
        return [(a['x']+a['w'],ay),((a['x']+a['w']+b['x'])/2,ay),((a['x']+a['w']+b['x'])/2,by),(b['x'],by)]
    return [(ax,a['y']+a['h']),(ax,max(a['y']+a['h'],b['y']+b['h'])+30),(bx,max(a['y']+a['h'],b['y']+b['h'])+30),(bx,b['y']+b['h'])]

def build(model):
    ident=model['id'];nodes={o['id']:o for o in model['nodes']};farmer=model['farmer'];nodes[farmer['id']]=farmer
    lanes=model['lanes'];top=150;lane_h=220
    for i,l in enumerate(lanes):
        l.setdefault('x',55);l.setdefault('y',top+i*lane_h);l.setdefault('w',1470);l.setdefault('h',lane_h)
    pool={'id':ident+'_Cooxupe','x':25,'y':min(l['y'] for l in lanes),'w':1500,
          'h':max(l['y']+l['h'] for l in lanes)-min(l['y'] for l in lanes)}
    annotations=model.get('annotations',[])
    height=max([pool['y']+pool['h']+85]+[a['y']+a['h']+30 for a in annotations]+[1000])
    defs=E.Element('{'+NS['bpmn']+'}definitions',nsmap=NS,id=ident+'_Definitions',targetNamespace='https://example.org/cooxupe/comparison')
    for msg in model.get('messages',[]):el(defs,'bpmn:message',id=msg['id']+'_Message',name=msg.get('name','Message'))
    proc=el(defs,'bpmn:process',id=ident+'_Process',name=model['title'],isExecutable='false')
    text(proc,'bpmn:documentation',model.get('subtitle','')+' Comparison proposal; assumptions and source limits are in NOTES.md.')
    lane_set=el(proc,'bpmn:laneSet',id=ident+'_LaneSet')
    for lane in lanes:
        element=el(lane_set,'bpmn:lane',id=lane['id'],name=lane['name'])
        for n in model['nodes']:
            if n['lane']==lane['id']:text(element,'bpmn:flowNodeRef',n['id'])
    types={'startMessage':'startEvent','end':'endEvent','gateway':'exclusiveGateway','timerCatch':'intermediateCatchEvent'}
    out=Counter(f['source'] for f in model['flows']);incoming=Counter(f['target'] for f in model['flows'])
    for n in model['nodes']:
        tag=types.get(n['type'],n['type']);attrs={'id':n['id'],'name':n['name']}
        if tag=='exclusiveGateway':attrs['gatewayDirection']='Diverging' if out[n['id']]>1 else 'Converging' if incoming[n['id']]>1 else 'Unspecified'
        e=el(proc,'bpmn:'+tag,**attrs)
        if n.get('documentation'):text(e,'bpmn:documentation',n['documentation'])
        for f in model['flows']:
            if f['target']==n['id']:text(e,'bpmn:incoming',f['id'])
        for f in model['flows']:
            if f['source']==n['id']:text(e,'bpmn:outgoing',f['id'])
        if n['type']=='startMessage':
            m=next((m for m in model.get('messages',[]) if m['target']==n['id']),None)
            a={'id':n['id']+'_Definition'}
            if m:a['messageRef']=m['id']+'_Message'
            el(e,'bpmn:messageEventDefinition',**a)
        elif n['type']=='timerCatch':
            t=el(e,'bpmn:timerEventDefinition',id=n['id']+'_Timer')
            q=text(t,'bpmn:timeDate',n.get('timeDate','scheduledVisitAt'));q.set('{'+NS['xsi']+'}type','bpmn:tFormalExpression')
        elif n['type']=='subProcess' and n.get('internal'):
            internal=n['internal']
            for child in internal['nodes']:
                attrs={'id':child['id']}
                if child.get('name'):attrs['name']=child['name']
                sub=el(e,'bpmn:'+child['type'],**attrs)
                for f in internal['flows']:
                    if f['target']==child['id']:text(sub,'bpmn:incoming',f['id'])
                for f in internal['flows']:
                    if f['source']==child['id']:text(sub,'bpmn:outgoing',f['id'])
            for f in internal['flows']:
                sub=el(e,'bpmn:sequenceFlow',id=f['id'],sourceRef=f['source'],targetRef=f['target'],name=f.get('name',''))
                if f.get('condition'):
                    c=text(sub,'bpmn:conditionExpression',f['condition']);c.set('{'+NS['xsi']+'}type','bpmn:tFormalExpression')
        elif n['type']=='subProcess':
            steps=n.get('subprocessSteps',['Perform advisory work'])
            ids=[n['id']+'_Start']+[n['id']+'_Step'+str(i+1) for i in range(len(steps))]+[n['id']+'_End']
            for i,subid in enumerate(ids):
                attrs={'id':subid}
                if 0<i<len(ids)-1:attrs['name']=steps[i-1]
                child=el(e,'bpmn:'+('startEvent' if i==0 else 'endEvent' if i==len(ids)-1 else 'task'),**attrs)
                if i:text(child,'bpmn:incoming',n['id']+'_Internal'+str(i))
                if i<len(ids)-1:text(child,'bpmn:outgoing',n['id']+'_Internal'+str(i+1))
            for i in range(len(ids)-1):el(e,'bpmn:sequenceFlow',id=n['id']+'_Internal'+str(i+1),sourceRef=ids[i],targetRef=ids[i+1])
    for f in model['flows']:
        e=el(proc,'bpmn:sequenceFlow',id=f['id'],sourceRef=f['source'],targetRef=f['target'],name=f.get('name',''))
        if f.get('condition'):
            c=text(e,'bpmn:conditionExpression',f['condition']);c.set('{'+NS['xsi']+'}type','bpmn:tFormalExpression')
    for a in annotations:
        e=el(proc,'bpmn:textAnnotation',id=a['id']);text(e,'bpmn:text',a['text'])
        if a.get('target'):el(proc,'bpmn:association',id=a['id']+'_Link',sourceRef=a['target'],targetRef=a['id'])
    collab=el(defs,'bpmn:collaboration',id=ident+'_Collaboration')
    el(collab,'bpmn:participant',id=farmer['id'],name=farmer['name'])
    el(collab,'bpmn:participant',id=pool['id'],name='Cooxupé · P1 Agricultural technical orientation',processRef=ident+'_Process')
    for m in model.get('messages',[]):el(collab,'bpmn:messageFlow',id=m['id'],name=m.get('name',''),sourceRef=m['source'],targetRef=m['target'],messageRef=m['id']+'_Message')
    diagram=el(defs,'bpmndi:BPMNDiagram',id=ident+'_Diagram');plane=el(diagram,'bpmndi:BPMNPlane',id=ident+'_Plane',bpmnElement=ident+'_Collaboration')
    def shape(obj,kind=None):
        attrs={'id':obj['id']+'_DI','bpmnElement':obj['id']}
        if kind=='pool' or kind=='lane':attrs['isHorizontal']='true'
        if obj.get('type')=='subProcess':attrs['isExpanded']='false'
        s=el(plane,'bpmndi:BPMNShape',**attrs);el(s,'dc:Bounds',x=obj['x'],y=obj['y'],width=obj['w'],height=obj['h'])
        if obj.get('type') in ['startMessage','end','timerCatch','gateway']:
            lx,ly=obj.get('labelPosition',[obj['x']+obj['w']/2,obj['y']+obj['h']+22]);label=el(s,'bpmndi:BPMNLabel');el(label,'dc:Bounds',x=lx-67,y=ly-18,width=134,height=46)
    shape(farmer,'pool');shape(pool,'pool')
    for l in lanes:shape(l,'lane')
    for n in model['nodes']:shape(n)
    for a in annotations:shape(a)
    edgepaths={}
    for f in model['flows']+model.get('messages',[]):
        points=f.get('waypoints') or route(nodes[f['source']],nodes[f['target']]);edgepaths[f['id']]=points
        edge=el(plane,'bpmndi:BPMNEdge',id=f['id']+'_DI',bpmnElement=f['id'])
        for x,y in points:el(edge,'di:waypoint',x=x,y=y)
        if f.get('name'):
            x,y=f.get('labelPosition',points[len(points)//2]);label=el(edge,'bpmndi:BPMNLabel');el(label,'dc:Bounds',x=x,y=y-10,width=140,height=25)
    for a in annotations:
        if a.get('target'):
            edge=el(plane,'bpmndi:BPMNEdge',id=a['id']+'_Link_DI',bpmnElement=a['id']+'_Link')
            for x,y in route(nodes[a['target']],a):el(edge,'di:waypoint',x=x,y=y)
    filename=ROOT/(ident.lower()+'.bpmn');filename.write_bytes(E.tostring(defs,pretty_print=True,xml_declaration=True,encoding='UTF-8'))
    # Render the same coordinates and identifiers, with standard BPMN symbols.
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="297mm" height="210mm" viewBox="0 0 1560 {height}">',
         '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#253746"/></marker><marker id="message" markerWidth="10" markerHeight="10" refX="9" refY="4" orient="auto"><path d="M1,0 L9,4 L1,8" fill="none" stroke="#526477"/></marker></defs>',
         '<rect width="1560" height="'+str(height)+'" fill="white"/>']
    def path(points,extra=''):
        d='M'+' L'.join(f'{x},{y}' for x,y in points);svg.append(f'<path d="{d}" fill="none" stroke="#253746" stroke-width="1.7" {extra}/>')
    def box(obj,fill='#fff',extra=''):
        x,y,w,h=rect(obj);svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#596977" stroke-width="1.2" {extra}/>')
    def label(value,x,y,width=110,font=15,align='middle',fill='#172b3a'):
        lines=[]
        for paragraph in str(value).split('\n'):lines.extend(textwrap.wrap(paragraph,max(9,int(width/(font*.51)))) or [''])
        lineheight=font*1.15;start=y-(len(lines)-1)*lineheight/2
        for i,line in enumerate(lines):svg.append(f'<text x="{x}" y="{start+i*lineheight}" text-anchor="{align}" dominant-baseline="middle" font-family="DejaVu Sans,sans-serif" font-size="{font}" fill="{fill}">{escape(line)}</text>')
    label(model['title'],25,20,1400,22,'start');label(model.get('subtitle',''),25,39,1480,11,'start')
    box(farmer,'#f4f6f8');label(farmer['name'],farmer['x']+farmer['w']/2,farmer['y']+farmer['h']/2,1000,18)
    box(pool,'#fff')
    for i,l in enumerate(lanes):
        box(l,'#f7fafd' if i%2==0 else '#fff')
        svg.append(f'<line x1="{l["x"]+38}" y1="{l["y"]}" x2="{l["x"]+38}" y2="{l["y"]+l["h"]}" stroke="#b6c1ca"/>')
        svg.append(f'<g transform="translate({l["x"]+20},{l["y"]+l["h"]/2}) rotate(-90)">');label(l['name'],0,0,l['h']-10,13);svg.append('</g>')
    svg.append(f'<g transform="translate(40,{pool["y"]+pool["h"]/2}) rotate(-90)">');label('Cooxupé · P1',0,0,pool['h']-10,15);svg.append('</g>')
    for f in model['flows']:
        points=edgepaths[f['id']];path(points,'marker-end="url(#arrow)"')
        if f.get('name'):
            x,y=f.get('labelPosition',points[len(points)//2]);label(f['name'],x,y,140,12,'start')
    for m in model.get('messages',[]):
        points=edgepaths[m['id']];path(points,'stroke-dasharray="7 5" marker-end="url(#message)"')
        x,y=points[0];svg.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="white" stroke="#526477"/>')
        if m.get('name'):
            x,y=m.get('labelPosition',points[len(points)//2]);label(m['name'],x,y,140,11,'start')
    for n in model['nodes']:
        x,y,w,h=rect(n);cx,cy=center(n);typ=n['type']
        if typ in ['startMessage','end','timerCatch']:
            radius=min(w,h)/2
            svg.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="white" stroke="#253746" stroke-width="{3.2 if typ=="end" else 1.6}"/>')
            if typ=='startMessage':
                svg.append(f'<rect x="{cx-10}" y="{cy-7}" width="20" height="14" fill="white" stroke="#253746"/>');path([(cx-10,cy-7),(cx,cy+1),(cx+10,cy-7)])
            if typ=='timerCatch':
                svg.append(f'<circle cx="{cx}" cy="{cy}" r="{radius-4}" fill="none" stroke="#253746"/>');path([(cx,cy-9),(cx,cy),(cx+7,cy+4)])
            lx,ly=n.get('labelPosition',[cx,y+h+21]);label(n['name'],lx,ly,134,13)
        elif typ=='gateway':
            svg.append(f'<path d="M{cx},{y} L{x+w},{cy} L{cx},{y+h} L{x},{cy} Z" fill="white" stroke="#253746" stroke-width="1.6"/>');path([(cx-7,cy-7),(cx+7,cy+7)]);path([(cx+7,cy-7),(cx-7,cy+7)])
            lx,ly=n.get('labelPosition',[cx,y+h+22]);label(n['name'],lx,ly,135,13)
        else:
            fill='#eaf3fb' if typ in ['serviceTask','businessRuleTask'] else '#fff'
            box(n,fill,'rx="9" ry="9"')
            if typ=='userTask':
                svg.append(f'<circle cx="{x+14}" cy="{y+11}" r="4" fill="none" stroke="#253746"/>');path([(x+8,y+23),(x+8,y+18),(x+20,y+18),(x+20,y+23)]);path([(x+14,y+15),(x+14,y+24)])
            elif typ=='serviceTask':
                for a in range(0,360,45):
                    rad=math.radians(a);path([(x+14+6*math.cos(rad),y+14+6*math.sin(rad)),(x+14+10*math.cos(rad),y+14+10*math.sin(rad))])
                svg.append(f'<circle cx="{x+14}" cy="{y+14}" r="6" fill="white" stroke="#253746"/>')
            elif typ=='businessRuleTask':
                svg.append(f'<rect x="{x+7}" y="{y+6}" width="19" height="17" fill="white" stroke="#253746"/>');path([(x+7,y+12),(x+26,y+12)]);path([(x+13,y+12),(x+13,y+23)]);path([(x+7,y+17),(x+26,y+17)])
            label(n['name'],cx,y+(h-18)/2 if typ=='subProcess' else y+(h+23)/2,w-15,14)
            if typ=='subProcess':
                svg.append(f'<rect x="{cx-6}" y="{y+h-16}" width="12" height="12" fill="white" stroke="#253746"/>');path([(cx-4,y+h-10),(cx+4,y+h-10)]);path([(cx,y+h-14),(cx,y+h-6)])
    for a in annotations:
        x,y,w,h=rect(a)
        if a.get('target'):path(route(nodes[a['target']],a),'stroke-dasharray="2 4"')
        path([(x+10,y),(x,y),(x,y+h),(x+10,y+h)])
        label(a['text'],x+12,y+h/2,w-20,12,'start')
    label('Comparison proposal · non-executable · assumptions and alignment notes: NOTES.md',25,height-18,1480,12,'start')
    svg.append('</svg>');svg_path=ROOT/(ident.lower()+'.svg');svg_path.write_text('\n'.join(svg))
    cairosvg.svg2png(url=str(svg_path),write_to=str(svg_path.with_suffix('.png')),output_width=2340,output_height=int(height*1.5))
    return filename,defs

def validate(path,root):
    ids=[e.get('id') for e in root.iter() if e.get('id')];assert len(ids)==len(set(ids)), 'Duplicate IDs'
    allids=set(ids)
    for e in root.iter():
        for attr in ['sourceRef','targetRef','processRef','messageRef','bpmnElement']:
            if e.get(attr):assert e.get(attr) in allids,(path,attr,e.get(attr))
        if E.QName(e).localname in ['flowNodeRef','incoming','outgoing']:assert e.text in allids
    for proc in root.findall('.//bpmn:process',NS)+root.findall('.//bpmn:subProcess',NS):
        direct={c.get('id') for c in proc if E.QName(c).localname!='laneSet'}
        for f in proc.findall('bpmn:sequenceFlow',NS):assert f.get('sourceRef') in direct and f.get('targetRef') in direct,'Flow crosses scope'
    schema_path=Path('/tmp/cooxupe-bpmn-xsd/BPMN20.xsd')
    if schema_path.exists():
        E.XMLSchema(E.parse(str(schema_path))).assertValid(E.parse(str(path)))
        schema_result='official XSD passed'
    else:
        schema_result='official XSD NOT RUN (schemas unavailable)'
    print(path.name,': references/scope passed;',schema_result)

if __name__=='__main__':
    data=json.loads((ROOT/'process-definitions.json').read_text())
    for model in data['models']:
        path,root=build(model);validate(path,root)
