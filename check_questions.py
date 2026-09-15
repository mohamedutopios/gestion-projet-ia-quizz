# -*- coding: utf-8 -*-
from collections import Counter
from questions import QUIZZES, QUIZ_ORDER
problems=0
for qid in QUIZ_ORDER:
    quiz=QUIZZES[qid]; letters=Counter(); longest_hits=0
    for n,item in enumerate(quiz["questions"],1):
        opts=item["options"]; ans=item["answer"]
        assert len(opts)==4, f"{qid} q{n}: pas 4 options"
        assert len(set(opts))==4, f"{qid} q{n}: options en double"
        letters[chr(65+ans)]+=1
        mx=max(len(o) for o in opts)
        if len(opts[ans])==mx and [len(o) for o in opts].count(mx)==1:
            longest_hits+=1; problems+=1
            print(f"  [X] {qid} q{n}: la bonne reponse est la PLUS LONGUE -> '{opts[ans][:50]}'")
    dist=dict(letters)
    # verifie qu'aucune lettre ne domine (> n/4 + 2)
    n=len(quiz["questions"]); lim=n//4+2
    for L,c in dist.items():
        if c>lim: problems+=1; print(f"  [X] {qid}: lettre {L} trop frequente ({c}/{n})")
    print(f"{qid}: repartition bonnes reponses {dist} | bonne reponse=plus longue: {longest_hits}")
print("\nRESULTAT:", "OK - toutes contraintes respectees" if problems==0 else f"{problems} probleme(s)")
