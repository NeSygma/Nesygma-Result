fof(distinct, axiom, (diamond_mine != roderick_strong & diamond_mine != creed_brothers & diamond_mine != ivy_nile & diamond_mine != imperium & roderick_strong != creed_brothers & roderick_strong != ivy_nile & roderick_strong != imperium & creed_brothers != ivy_nile & creed_brothers != imperium & ivy_nile != imperium)).
fof(p1, axiom, stable(diamond_mine)).
fof(p2, axiom, leads(roderick_strong, diamond_mine)).
fof(p3, axiom, includes(diamond_mine, creed_brothers) & includes(diamond_mine, ivy_nile)).
fof(p4, axiom, has_feud(imperium, diamond_mine)).
fof(goal, conjecture, ? [S] : (stable(S) & includes(S, ivy_nile) & has_feud(imperium, S))).