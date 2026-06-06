fof(distinct_entities, axiom, (roderick_strong != diamond_mine & roderick_strong != creed_brothers & roderick_strong != ivy_nile & roderick_strong != imperium & roderick_strong != wwe & diamond_mine != creed_brothers & diamond_mine != ivy_nile & diamond_mine != imperium & diamond_mine != wwe & creed_brothers != ivy_nile & creed_brothers != imperium & creed_brothers != wwe & ivy_nile != imperium & ivy_nile != wwe & imperium != wwe)).
fof(premise_1, axiom, stable(diamond_mine)).
fof(premise_2, axiom, leads(roderick_strong, diamond_mine)).
fof(premise_3, axiom, includes(diamond_mine, creed_brothers)).
fof(premise_4, axiom, includes(diamond_mine, ivy_nile)).
fof(premise_5, axiom, has_feud(imperium, diamond_mine)).
fof(goal, conjecture, ~(? [X] : (stable(X) & leads(roderick_strong, X)))).