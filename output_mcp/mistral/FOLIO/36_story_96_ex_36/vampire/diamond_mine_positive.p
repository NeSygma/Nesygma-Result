fof(diamond_mine_is_stable, axiom, stable(diamond_mine)).
fof(roderick_leads_diamond_mine, axiom, leads(roderick_strong, diamond_mine)).
fof(diamond_mine_includes_creed, axiom, includes(diamond_mine, creed_brothers)).
fof(diamond_mine_includes_ivy, axiom, includes(diamond_mine, ivy_nile)).
fof(imperium_feuds_with_diamond_mine, axiom, feuds_with(imperium, diamond_mine)).
fof(conclusion_claim, conjecture, ~(? [S] : (stable(S) & includes(S, ivy_nile) & feuds_with(imperium, S)))).