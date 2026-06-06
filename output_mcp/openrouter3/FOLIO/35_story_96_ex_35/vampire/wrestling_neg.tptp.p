% Wrestling premises and negated conclusion
fof(premise_1, axiom, stable(diamond_mine)).
fof(premise_2, axiom, formed_in(diamond_mine, wwe)).
fof(premise_3, axiom, leads(roderick_strong, diamond_mine)).
fof(premise_4, axiom, includes(diamond_mine, creed_brothers)).
fof(premise_5, axiom, includes(diamond_mine, ivy_nile)).
fof(premise_6, axiom, has_feud(imperium, diamond_mine)).
fof(negated_conclusion, conjecture, ~leads(roderick_strong, creed_brothers)).