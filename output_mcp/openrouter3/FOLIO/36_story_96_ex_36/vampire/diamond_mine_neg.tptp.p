% Diamond Mine problem - Negative version (negated conclusion)
fof(premise_1, axiom, stable(diamond_mine)).
fof(premise_2, axiom, leads(roderick_strong, diamond_mine)).
fof(premise_3, axiom, includes(diamond_mine, creed_brothers)).
fof(premise_4, axiom, includes(diamond_mine, ivy_nile)).
fof(premise_5, axiom, has_feud(imperium, diamond_mine)).
fof(distinct_entities, axiom, (diamond_mine != imperium & diamond_mine != ivy_nile & imperium != ivy_nile & diamond_mine != creed_brothers & imperium != creed_brothers & ivy_nile != creed_brothers)).
fof(goal_negated, conjecture, has_feud(imperium, diamond_mine) & includes(diamond_mine, ivy_nile)).