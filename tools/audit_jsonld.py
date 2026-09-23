#!/usr/bin/env python3
import argparse,json
from html.parser import HTMLParser
from pathlib import Path
class P(HTMLParser):
 def __init__(self): super().__init__(); self.on=False; self.buf=[]; self.blocks=[]
 def handle_starttag(self,tag,attrs):
  if tag.lower()=='script' and dict(attrs).get('type','').lower()=='application/ld+json': self.on=True; self.buf=[]
 def handle_data(self,data):
  if self.on: self.buf.append(data)
 def handle_endtag(self,tag):
  if tag.lower()=='script' and self.on: self.blocks.append(''.join(self.buf)); self.on=False
def nodes(x):
 if isinstance(x,list):
  for v in x: yield from nodes(v)
 elif isinstance(x,dict):
  if '@graph' in x: yield from nodes(x['@graph'])
  yield x
def types(n):
 t=n.get('@type',[]); return {t} if isinstance(t,str) else set(t) if isinstance(t,list) else set()
def author_ok(a):
 if isinstance(a,str): return bool(a.strip())
 if isinstance(a,dict): return bool(str(a.get('name','')).strip() or str(a.get('@id','')).strip())
 if isinstance(a,list): return bool(a) and all(author_ok(x) for x in a)
 return False
def audit(path,required=None):
 p=P(); p.feed(Path(path).read_text(encoding='utf-8')); errors=[]; parsed=[]
 if not p.blocks: return ['no JSON-LD blocks found']
 for i,b in enumerate(p.blocks,1):
  try: parsed.append(json.loads(b))
  except json.JSONDecodeError as e: errors.append(f'block {i}: invalid JSON-LD: {e.msg}')
 ns=[n for doc in parsed for n in nodes(doc)]
 if required and not any(required in types(n) for n in ns): errors.append(f'required type not found: {required}')
 article={'Article','NewsArticle','BlogPosting'}
 for i,n in enumerate(ns,1):
  if types(n)&article:
   if not str(n.get('headline','')).strip(): errors.append(f'node {i}: article-like node missing headline')
   if not author_ok(n.get('author')): errors.append(f'node {i}: article-like node missing usable author')
   if not str(n.get('datePublished','')).strip(): errors.append(f'node {i}: article-like node missing datePublished')
 return errors
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('html'); ap.add_argument('--require-type'); a=ap.parse_args(); e=audit(a.html,a.require_type)
 if e:
  for x in e: print('ERROR:',x)
  return 1
 print('OK: JSON-LD audit passed'); return 0
if __name__=='__main__': raise SystemExit(main())
