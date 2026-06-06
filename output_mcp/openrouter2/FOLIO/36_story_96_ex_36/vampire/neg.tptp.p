fof(distinct, axiom, (diamond_mine != roderick_strong & diamond_mine != creed_brothers & diamond_mine != ivy_nile & diamond_mine != imperium & roderick_strong != creed_brothers & roderick_strong != ivy_nile & roderick_strong != imperium & creed_brothers != ivy_nile & creed_brothers != imperium & ivy_nile != imperium)).
fof(stable_diamond, axiom, stable(diamond_mine)).
fof(stable_imperium, axiom, stable(imperium)).
fof(member_creed, axiom, member_of(creed_brothers, diamond_mine)).
fof(member_ivy, axiom, member_of(ivy_nile, diamond_mine)).
fof(leads, axiom, leads(roderick_strong, diamond_mine)).
fof(feud, axiom, feud(imperium, diamond_mine)).
fof(conclusion, conjecture, ? [S] : (stable(S) & member_of(ivy_nile, S) & feud(imperium, S))).