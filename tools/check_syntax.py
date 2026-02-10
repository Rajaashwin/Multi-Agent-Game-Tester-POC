import py_compile
from pathlib import Path
import sys
errs = []
for p in Path('.').rglob('*.py'):
    if 'venv' in p.parts or 'venv_new' in p.parts:
        continue
    try:
        py_compile.compile(str(p), doraise=True)
    except Exception as e:
        errs.append((str(p), str(e)))
        print('SYNTAX ERROR in', p, e)
print('Done. Errors:', len(errs))
if errs:
    sys.exit(1)
