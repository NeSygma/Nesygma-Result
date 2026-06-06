% Positive version
fof(premise1, axiom, stable(diamond_mine)).
fof(premise2, axiom, leads(rod_strong, diamond_mine)).
fof(premise3, axiom, includes(diamond_mine, creed_brothers)).
fof(premise4, axiom, includes(diamond_mine, ivy_nile)).
fof(premise5, axiom, feud(imperium, diamond_mine)).
fof(distinct, axiom, (diamond_mine != rod_strong & diamond_mine != creed_brothers & diamond_mine != ivy_nile & diamond_mine != imperium & rod_strong != creed_brothers & rod_strong != ivy_nile & rod_strong != imperium & creed_brothers != ivy_nile & creed_brothers != imperium & ivy_nile != imperium)).
fof(goal, conjecture, leads(rod_strong, creed_brothers)).