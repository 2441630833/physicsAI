import json, os, re, time, urllib.error, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
queries = {'all':'all:"physical AI" OR all:"world model" OR all:"embodied AI" OR all:"physics informed"', 'physical':'all:"physical AI" OR all:"physics informed" OR all:"robot learning" OR all:"embodied AI"', 'world':'all:"world model" OR all:"world models" OR all:"video prediction"'}
ns={'a':'http://www.w3.org/2005/Atom','o':'http://a9.com/-/spec/opensearch/1.1/'}
data={'updated':datetime.now(timezone.utc).isoformat(),'topics':{}}
verified = {}
def accessible_repo(owner, repo):
 key=(owner.lower(), repo.lower())
 if key not in verified:
  headers={'User-Agent':'PhysicalArchive/1.0','Accept':'application/vnd.github+json'}
  if os.environ.get('GITHUB_TOKEN'): headers['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
  req=urllib.request.Request('https://api.github.com/repos/'+owner+'/'+repo,headers=headers)
  try:
   with urllib.request.urlopen(req,timeout=25) as response: result=json.load(response)
   verified[key]=result.get('html_url') if not result.get('private',True) and result.get('size',0)>0 else None
  except urllib.error.HTTPError as e:
   if e.code in (404, 410): verified[key]=None
   else: raise
 return verified[key]
def find_repo(summary):
 for match in re.finditer(r'https?://(?:www\.)?github\.com/([A-Za-z0-9_-]+)/([A-Za-z0-9_.-]+)', summary, re.I):
  owner,repo=match.groups(); repo=repo.rstrip('.,;:')
  if repo.endswith('.git'): repo=repo[:-4]
  if repo:
   url=accessible_repo(owner,repo)
   if url: return url
 return None
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
  github=find_repo(get('summary'))
  papers.append({'github':github,'title':get('title'),'summary':get('summary'),'published':get('published')[:10],'url':url,'id':url.split('/abs/')[-1], 'authors':[a.findtext('a:name',default='',namespaces=ns) for a in e.findall('a:author',ns)],'categories':[c.get('term') for c in e.findall('a:category',ns)]})
 if not root.findall('a:entry',ns): raise RuntimeError('No arXiv results returned for '+topic)
 papers.sort(key=lambda paper: bool(paper['github']), reverse=True)
 data['topics'][topic]=papers
Path('pages/papers.json').write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')

