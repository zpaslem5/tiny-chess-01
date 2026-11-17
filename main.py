import json,os,base64,urllib.request as R
U=os.environ["MAKEFUN_ENV_URL"]
N=int(os.environ.get("CHESS_NODES","50000"))
V=(0,100,320,330,500,900,0)
T=[b-50 for b in base64.b64decode("MjIyMjc8PB43LSgyMjIyRjc3PEs8PEZQZGRkZDIyMjIAChQUCh4yNxQ3PEEUMkFGFDdBRhQyPEEKHjIyAAoUFEZQPDJGRjIyKB4eHh4UFAoUCgoAFAoKABQKCgAUCgoA")]
B=[0]*128;W=1;C=0;Y=-1;nd=0
Z={4:3,116:12,7:1,0:2,119:4,112:8}
O=(1,-1,16,-16,15,17,-15,-17);Q=(31,33,14,18,-31,-33,-14,-18);D={2:Q,6:O,3:O[4:],4:O[:4],5:O}
def F(f):
 global W,C,Y,KW,KB
 p=f.split();B[:]=[0]*128;s=112
 for ch in p[0]:
  if ch=="/":s-=24
  elif ch.isdigit():s+=int(ch)
  else:
   B[s]=" PNBRQK".index(ch) if ch.isupper() else -" pnbrqk".index(ch)
   if ch=="K":KW=s
   elif ch=="k":KB=s
   s+=1
 W=1 if p[1]=="w" else -1
 C=sum((ch in p[2])<<i for i,ch in enumerate("KQkq"))
 Y=-1 if p[3]=="-" else (ord(p[3][0])-97)+((int(p[3][1])-1)<<4)
def A(s,c):
 d=-16 if c>0 else 16
 for f in(-1,1):
  t=s+d+f
  if not t&136 and B[t]==c:return 1
 for d in Q:
  t=s+d
  if not t&136 and B[t]==c*2:return 1
 for d in O:
  t=s+d
  if not t&136 and B[t]==c*6:return 1
 for d in O:
  t=s+d;q=3 if d in O[4:] else 4
  while not t&136:
   p=B[t]
   if p:
    if p==c*q or p==c*5:return 1
    break
   t+=d
 return 0
def I():return A(KW if W<0 else KB,W)
def G(c):
 M=[]
 for s in range(128):
  p=B[s]
  if not p or (p>0)!=(W>0):continue
  a=abs(p)
  if a==1:
   d=16*W;t=s+d
   if not t&136 and not B[t] and not c:
    if t>>4 in(0,7):M+=[(s,t,q,0) for q in(5,4,3,2)]
    else:
     M.append((s,t,0,0))
     if (s>>4)==(1 if W>0 else 6) and not B[s+2*d]:M.append((s,s+2*d,0,4))
   for f in(-1,1):
    t=s+d+f
    if t&136:continue
    q=B[t]
    if (q and (q>0)!=(W>0)) or t==Y:
     M+=[(s,t,x,0) for x in(5,4,3,2)] if t>>4 in(0,7) else [(s,t,0,1 if t==Y else 0)]
  elif a in D:
   for d in D[a]:
    t=s+d
    while not t&136:
     q=B[t]
     if q:
      if (q>0)!=(W>0):M.append((s,t,0,0))
      break
     if not c:M.append((s,t,0,0))
     if a in(2,6):break
     t+=d
  if a==6:
   for d,b in((1,1 if W>0 else 4),(-1,2 if W>0 else 8)):
    if C&b and not(B[s+d] or B[s+2*d]) and (d>0 or not B[s-3]) and B[s+3*d if d>0 else s-4]==4*W and not(A(s,-W) or A(s+d,-W) or A(s+2*d,-W)):M.append((s,s+2*d,0,2))
 return M
def K(m):
 global W,C,Y,KW,KB
 s,t,p,f=m;pc=B[s];cp=B[t];u=(pc,cp,C,Y)
 B[t]=p*W if p else pc;B[s]=0
 if abs(pc)==6:
  if W>0:KW=t
  else:KB=t
 if f==1:B[t-16*W]=0
 if f==2:
  a,b=(t+1,t-1) if t in(6,118) else (t-2,t+1);B[b]=B[a];B[a]=0
 for q in(s,t):
  if q in Z:C&=~Z[q]
 Y=s+16*W if f==4 else -1
 W=-W
 return u
def J(m,u):
 global W,C,Y,KW,KB
 s,t,p,f=m;pc,cp,c0,y0=u
 W=-W;C=c0;Y=y0
 B[s]=pc;B[t]=cp
 if abs(pc)==6:
  if W>0:KW=s
  else:KB=s
 if f==1:B[t-16*W]=-W
 if f==2:
  a,b=(t+1,t-1) if t in(6,118) else (t-2,t+1);B[a]=B[b];B[b]=0
def E():
 sc=0
 for s in range(128):
  p=B[s]
  if p:
   a=abs(p);r=s>>4;f=s&7;g=min(f,7-f);i=(0,32,0,0,0,64)[a-1]+(r if p>0 else 7-r)*4+g
   sc+=(V[a]+(T[i] if a in(1,2,6) else 0))*(p//a)
 return sc if W>0 else -sc
def S(a,b,d):
 global nd
 nd+=1
 if nd>N:raise StopIteration
 if d<=0:
  s=E()
  if s>=b:return b
  if s>a:a=s
 ms=sorted(G(d<=0),key=lambda m:-abs(B[m[1]]))
 for m in ms:
  u=K(m)
  if I():J(m,u);continue
  v=-S(-b,-a,max(d-1,0));J(m,u)
  if v>=b:return b
  if v>a:a=v
 return a
def M(L):
 global nd
 nd=0
 ms=[m for m in G(0) if not (lambda u:(I(),J(m,u))[0])(K(m))]
 if not ms:return L[0]
 best=ms[0]
 try:
  for d in range(1,9):
   bv=-9999;bb=ms[0]
   for m in ms:
    u=K(m);v=-S(-9999,9999,d-1);J(m,u)
    if v>bv:bv=v;bb=m
   best=bb
 except StopIteration:pass
 s,t,p,f=best
 u=chr(97+(s&7))+str(s//16+1)+chr(97+(t&7))+str(t//16+1)+("nbrq"[p-2] if p else "")
 return u if u in L else L[0]
def P(p,m):
 try:
  q=R.Request(U+p,json.dumps(m).encode(),{"Content-Type":"application/json"})
  with R.urlopen(q,timeout=10) as r:return json.load(r)
 except Exception:return {}
while True:
 g=P("/game",{})
 if g.get("status")=="done":break
 while g.get("status")=="your_move":
  F(g["fen"]);g=P("/move",{"game":g["game"],"move":M(g["legal_moves"])})
