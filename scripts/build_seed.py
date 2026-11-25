import openpyxl,sys,warnings,json,datetime,collections,re
warnings.simplefilter('ignore')
wb=openpyxl.load_workbook(sys.argv[1],data_only=True)
def d(v):
    if isinstance(v,datetime.datetime): return v.date().isoformat()
    if isinstance(v,str):
        m=re.match(r'(\d\d)/(\d\d)/(\d{4})',v.strip())
        if m: return f'{m[3]}-{m[2]}-{m[1]}'
    return None
def n(v):
    try: return round(float(v),2) if v not in (None,'','-') else None
    except: return None
def s(v): return re.sub(r'\s+',' ',str(v).replace('\xa0',' ')).strip() if v not in (None,) else ''
# carteiras
tr={}
for r in wb['Trainer e recruta'].iter_rows(min_row=2,values_only=True):
    if r[2]: tr.setdefault(s(r[2]).upper(),(s(r[7]),s(r[8])))
cart={}
for r in wb['DEXPARA'].iter_rows(min_row=2,values_only=True):
    if not r[9]: continue
    k=s(r[9])
    if k.upper() in {c.upper() for c in cart}: continue
    t=tr.get(k.upper(),('',''))
    cart[k]=dict(nome=k,superintendente=s(r[0]),conta=s(r[1]),cidade=s(r[2]),activity=s(r[4]) or s(r[3]),actId=s(r[5]),endereco=s(r[6]),andar=s(r[7]),agrupamento=s(r[8]),
        diasTreino=int(n(r[11]) or n(r[10]) or 0),treinador=t[0],recrutamento=t[1])
fer=[]
for r in wb['DEXPARA'].iter_rows(min_row=2,values_only=True):
    if r[19] and d(r[19]): fer.append(dict(data=d(r[19]),nome=s(r[20]).split(': ',1)[-1]))
# candidatos
g=collections.defaultdict(list)
for r in wb['CONTROLE REQUISIÇÕES '].iter_rows(min_row=2,values_only=True):
    if r[0]: g[s(r[0])].append(r)
cands={k:[dict(id=str(x[2]),s='NO SHOW' if 'NO' in s(x[1]).upper() else 'PRESENTE') for x in v] for k,v in g.items() if all(x[2] for x in v)}
st={'ABERTA':'ABERTO','CANCELADO':'CANCELADA','MIGRADOS/ INTERNA':'MIGRADO/INTERNA'}
reqs=[]
for i,r in enumerate(wb['CONSOLIDADO'].iter_rows(min_row=2,values_only=True)):
    if not r[3]: continue
    wd=s(r[3]); cn=s(r[7]); c=cart.get(cn,{})
    status=st.get(s(r[4]).upper(),s(r[4]).upper())
    just=s(r[5]); just='' if just=='-' else just
    nec=n(r[8]) or 0; buf=n(r[9]) or 0
    sel=n(r[11]); ns=n(r[12]); pr=n(r[13])
    ab=d(r[15]); ini=d(r[16]); alo=d(r[17])
    rec=dict(wd=wd,status=status,carteira=cn,superintendente=s(r[2]) or c.get('superintendente',''),cidade=s(r[6]) or c.get('cidade',''),
        necessidade=nec,buffer=buf,selecionados=sel,noShow=ns,presente=pr,abertura=ab,inicioTreino=ini,alo=alo,
        diasTreino=int(n(r[18]) or c.get('diasTreino') or 0),aloManual=True,
        hist=[dict(t=just,d=ab or '',tipo='nota',imp=True)] if just else [],
        candidatos=cands.get(wd,[]),origem='planilha',criadoEm=ab or '')
    reqs.append(rec)
for cn in {r['carteira'] for r in reqs}-set(cart):
    ex=next(r for r in reqs if r['carteira']==cn)
    cart[cn]=dict(nome=cn,superintendente=ex['superintendente'],conta='',cidade=ex['cidade'],activity='',actId='',endereco='',andar='',agrupamento='',diasTreino=ex['diasTreino'],treinador='',recrutamento='')
json.dump(dict(carteiras=list(cart.values()),feriados=fer,reqs=reqs),open(sys.argv[2],'w'),ensure_ascii=False,separators=(',',':'))
print(len(reqs),len(cart),len(fer),sum(1 for r in reqs if r['candidatos']), collections.Counter(r['status'] for r in reqs))
