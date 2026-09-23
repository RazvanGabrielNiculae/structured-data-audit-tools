import subprocess,sys,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]; T=R/'tools'/'audit_jsonld.py'
def run(rel,*args): return subprocess.run([sys.executable,str(T),str(R/rel),*args],capture_output=True,text=True)
class Audit(unittest.TestCase):
 def test_valid_article(self): self.assertEqual(run('examples/article.html','--require-type','Article').returncode,0)
 def test_malformed_json(self): self.assertNotEqual(run('tests/fixtures/malformed.html').returncode,0)
 def test_missing_author(self): self.assertNotEqual(run('tests/fixtures/missing-author.html').returncode,0)
 def test_required_type(self): self.assertNotEqual(run('tests/fixtures/wrong-type.html','--require-type','Article').returncode,0)
if __name__=='__main__': unittest.main()
