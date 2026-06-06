fof(premise1, axiom, stable(diamond_mine)).
fof(premise2, axiom, leads(roderick_strong, diamond_mine)).
fof(premise3a, axiom, includes(diamond_mine, creed_brothers)).
fof(premise3b, axiom, includes(diamond_mine, ivy_nile)).
fof(premise4, axiom, has_feud(imperium, diamond_mine)).
fof(distinct_constants, axiom, (diamond_mine != roderick_strong & diamond_mine != creed_brothers & diamond_mine != ivy_nile & diamond_mine != imperium & roderick_strong != creed_brothers & roderick_strong != ivy_nile & roderick_strong != imperium & creed_brothers != ivy_nile & creed_brothers != imperium & ivy_nile != imperium)).
fof(goal_neg, conjecture, ~? [X] : (stable(X) & leads(roderick_strong, X))).