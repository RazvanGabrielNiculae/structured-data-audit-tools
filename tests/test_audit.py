import importlib.util,pathlib,tempfile,unittest,json
P=pathlib.Path(__file__).parents[1]/'tools'/'audit_jsonld.py'; s=importlib.util.spec_from_file_location('m',P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def f(obj): q=tempfile.NamedTemporaryFile('w',delete=False,suffix='.html'); q.write('<script type="application/ld+json">'+json.dumps(obj)+'</script>'); q.close(); return q.name
class T(unittest.TestCase):
 def test_nested_article_and_refs(self):
  o={'@graph':[{'@id':'#p','@type':'Person','name':'A'},{'@id':'#o','@type':'Organization','name':'O'},{'@type':'WebPage','mainEntity':{'@type':'Article','headline':'H','author':{'@id':'#p'},'publisher':{'@id':'#o'},'datePublished':'2026-01-01'}}]}; self.assertEqual(m.audit(f(o),'Article'),[])
 def test_dangling_author(self):
  o={'@type':'Article','headline':'H','author':{'@id':'#missing'},'publisher':{'name':'O'},'datePublished':'2026-01-01'}; self.assertTrue(any('author' in x for x in m.audit(f(o))))
 def test_missing_publisher(self):
  o={'@type':'Article','headline':'H','author':{'name':'A'},'datePublished':'2026-01-01'}; self.assertTrue(any('publisher' in x for x in m.audit(f(o))))
 def test_required_nested_type(self): self.assertFalse(any('required type' in x for x in m.audit(f({'mainEntity':{'@type':'Article','headline':'H','author':{'name':'A'},'publisher':{'name':'O'},'datePublished':'2026-01-01'}}),'Article')))
if __name__=='__main__':unittest.main()
