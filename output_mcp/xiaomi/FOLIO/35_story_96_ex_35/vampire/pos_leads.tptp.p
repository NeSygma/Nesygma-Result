fof(entity_dm, axiom, diamond_mine != roderick_strong).
fof(entity_cb, axiom, diamond_mine != creed_brothers).
fof(entity_in, axiom, diamond_mine != imperium).
fof(entity_rs, axiom, roderick_strong != creed_brothers).
fof(entity_rs2, axiom, roderick_strong != imperium).
fof(entity_cb2, axiom, creed_brothers != imperium).
fof(entity_in2, axiom, ivy_nile != diamond_mine).
fof(entity_in3, axiom, ivy_nile != roderick_strong).
fof(entity_in4, axiom, ivy_nile != creed_brothers).
fof(entity_in5, axiom, ivy_nile != imperium).

fof(premise_1, axiom, leads(roderick_strong, diamond_mine)).
fof(premise_2, axiom, includes(diamond_mine, creed_brothers)).
fof(premise_3, axiom, includes(diamond_mine, ivy_nile)).
fof(premise_4, axiom, feud_with(imperium, diamond_mine)).

fof(goal, conjecture, leads(roderick_strong, creed_brothers)).