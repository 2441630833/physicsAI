import json, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
queries = {'all':'all:"physical AI" OR all:"world model" OR all:"embodied AI" OR all:"physics informed"', 'physical':'all:"physical AI" OR all:"physics informed" OR all:"robot learning" OR all:"embodied AI"', 'world':'all:"world model" OR all:"world models" OR all:"video prediction"'}
ns={'a':'http://www.w3.org/2005/Atom','o':'http://a9.com/-/spec/opensearch/1.1/'}
data={'updated':datetime.now(timezone.utc).isoformat(),'topics':{}}
for index,(topic,query) in enumerate(queries.items()):
 if index: time.sleep(3)
 params=urllib.parse.urlencode({'search_query':query,'start':0,'max_results':100,'sortBy':'submittedDate','sortOrder':'descending'})
 req=urllib.request.Request('https://export.arxiv.org/api/query?'+params,headers={'User-Agent':'PhysicalArchive/1.0 (academic discovery)'})
 with urllib.request.urlopen(req,timeout=45) as response: root=ET.fromstring(response.read())
 papers=[]
 for e in root.findall('a:entry',ns):
  get=lambda name:' '.join(e.findtext('a:'+name,default='',namespaces=ns).split())
  url=get('id').replace('http://','https://')
  if not url.startswith('https://arxiv.org/abs/'): continue
  papers.append({'title':get('title'),'summary':get('summary'),'published':get('published')[:10],'url':url,'id':url.split('/abs/')[-1], 'authors':[a.findtext('a:name',default='',namespaces=ns) for a in e.findall('a:author',ns)],'categories':[c.get('term') for c in e.findall('a:category',ns)]})
 if not papers: raise RuntimeError('No papers returned for '+topic)
 data['topics'][topic]=papers
Path('pages/papers.json').write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
