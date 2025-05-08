import os
tests = ['test50k.max', 'test100k.max', 'test150k.max', 'test200k.max', 'test300k.max']
for t in tests:
    os.system(f'pypy3 algorithms.py tests/{t}')
