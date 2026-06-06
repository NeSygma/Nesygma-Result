fof(leads_axiom, axiom, leads(roderick_strong, diamond_mine)).
fof(includes_creed, axiom, includes_member(diamond_mine, creed_brothers)).
fof(includes_ivy, axiom, includes_member(diamond_mine, ivy_nile)).
fof(feud_axiom, axiom, has_feud(imperium, diamond_mine)).
fof(conclusion_negation, conjecture, ? [S] : (has_feud(imperium, S) & includes_member(S, ivy_nile))).