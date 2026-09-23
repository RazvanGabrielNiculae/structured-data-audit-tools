#!/usr/bin/env python3
import argparse,json
from html.parser import HTMLParser
from pathlib import Path
class P(HTMLParser):
 def __init__(self): super().__init__(); self.on=False; self.buf=[]; self.blocks=[]
 def handle_starttag(self,tag,attrs):
  if tag.lower()=='script' and (dict(attrs).get('type') or '').lower()=='application/ld+json': self.on=True; self.buf=[]
 def handle_data(self,data):
  if self.on:self.buf.append(data)
 def handle_endtag(self,tag):
  if tag.lower()=='script' and self.on:self.blocks.append(''.join(self.buf)); self.on=False
def nodes(x):
 if isinstance(x,list):
  for v in x: yield from nodes(v)
 elif isinstance(x,dict):
  yield x
  for k,v in x.items():
   if k not in ('@context',): yield from nodes(v)
def types(n):
 t=n.get('@type',[]); return {t} if isinstance(t,str) else set(t) if isinstance(t,list) else set()
def identity_ok(v,index):
 if isinstance(v,str): return bool(v.strip())
 if isinstance(v,list): return bool(v) and all(identity_ok(x,index) for x in v)
 if isinstance(v,dict):
  if str(v.get('name','')).strip(): return True
  ref=str(v.get('@id','')).strip(); return bool(ref and ref in index and (str(index[ref].get('name','')).strip() or types(index[ref])&{'Person','Organization'}))
 return False
def audit(path,required=None):
 p=P(); p.feed(Path(path).read_text(encoding='utf-8')); errors=[]; parsed=[]
 if not p.blocks:return ['no JSON-LD blocks found']
 for i,b in enumerate(p.blocks,1):
  try:parsed.append(json.loads(b))
  except json.JSONDecodeError as e:errors.append(f'block {i}: invalid JSON-LD: {e.msg}')
 ns=[n for d in parsed for n in nodes(d)]; index={}
 for n in ns:
  if isinstance(n,dict) and n.get('@id'):
   k=str(n.get('@id'))
   if k not in index or len(n)>len(index[k]): index[k]=n
 if required and not any(required in types(n) for n in ns):errors.append(f'required type not found: {required}')
 article={'Article','NewsArticle','BlogPosting'}
 for i,n in enumerate(ns,1):
  if types(n)&article and any(k in n for k in ('headline','author','publisher','datePublished')):
   if not str(n.get('headline','')).strip():errors.append(f'node {i}: article-like node missing headline')
   if not identity_ok(n.get('author'),index):errors.append(f'node {i}: article-like node missing resolvable author')
   if not str(n.get('datePublished','')).strip():errors.append(f'node {i}: article-like node missing datePublished')
   if not identity_ok(n.get('publisher'),index):errors.append(f'node {i}: article-like node missing resolvable publisher')
 return errors
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('html'); ap.add_argument('--require-type'); n=ap.parse_args(); e=audit(n.html,n.require_type)
 for x in e:print('ERROR:',x)
 if not e:print('OK: JSON-LD audit passed')
 return 1 if e else 0
if __name__=='__main__':raise SystemExit(main())
