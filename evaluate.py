"""Run the included 30-case transparent baseline evaluation."""
import csv
from core import fallback

def cer(ref, hyp):
    prev=list(range(len(hyp)+1))
    for i,a in enumerate(ref,1):
        cur=[i]
        for j,b in enumerate(hyp,1): cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(a!=b)))
        prev=cur
    return prev[-1]/max(1,len(ref))

rows=list(csv.DictReader(open("evaluation_cases.csv",encoding="utf-8-sig")))
scores=[cer(r["reference"],fallback(r["input"])) for r in rows]
print(f"cases={len(rows)}; exact-match accuracy={sum(x==0 for x in scores)/len(scores):.1%}; mean CER={sum(scores)/len(scores):.3f}")
print("Scope: closed lexicon baseline only; not an IndicXlit benchmark.")
