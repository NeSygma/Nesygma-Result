fof(diamond_mine_is_stable, axiom, professional_wrestling_stable(diamond_mine)).
fof(diamond_mine_formed_wwe, axiom, formed_in_wwe(diamond_mine)).
fof(roderick_leads_diamond_mine, axiom, leads(roderick_strong, diamond_mine)).
fof(diamond_mine_includes_creed, axiom, includes(diamond_mine, creed_brothers)).
fof(diamond_mine_includes_ivy, axiom, includes(diamond_mine, ivy_nile)).
fof(imperium_feud_diamond_mine, axiom, has_feud(imperium, diamond_mine)).
fof(goal, conjecture, ~? [X] : (professional_wrestling_stable(X) & leads(roderick_strong, X))).