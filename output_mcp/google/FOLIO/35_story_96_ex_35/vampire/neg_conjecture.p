fof(stable_def, axiom, is_stable(diamond_mine)).
fof(leader_def, axiom, leads(roderick_strong, diamond_mine)).
fof(includes_def1, axiom, includes(diamond_mine, creed_brothers)).
fof(includes_def2, axiom, includes(diamond_mine, ivy_nile)).
fof(feud_def, axiom, feud(imperium, diamond_mine)).
fof(distinct, axiom, (roderick_strong != diamond_mine & roderick_strong != creed_brothers & roderick_strong != ivy_nile & roderick_strong != imperium & diamond_mine != creed_brothers & diamond_mine != ivy_nile & diamond_mine != imperium & creed_brothers != ivy_nile & creed_brothers != imperium & ivy_nile != imperium)).
fof(goal, conjecture, ~leads(roderick_strong, creed_brothers)).