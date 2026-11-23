import json,sys,urllib.request,os
for line in open('items.tsv'):
    k,ident=line.split()
    out='raw/%s.txt'%k
    if os.path.exists(out) and os.path.getsize(out)>1000: continue
    try:
        md=json.load(urllib.request.urlopen('https://archive.org/metadata/%s'%ident,timeout=60))
        fs=[f['name'] for f in md.get('files',[]) if f['name'].endswith('_djvu.txt')]
        if not fs: print(k,'NO djvu', [f['name'] for f in md.get('files',[])][:8]); continue
        data=urllib.request.urlopen('https://archive.org/download/%s/%s'%(ident,urllib.request.quote(fs[0])),timeout=120).read()
        open(out,'wb').write(data); print(k,len(data))
    except Exception as e: print(k,'ERR',e)
