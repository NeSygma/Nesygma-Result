fof(diamond_mine_is_stable, axiom, wrestling_stable(diamond_mine)).
fof(roderick_leads_dm, axiom, leads(roderick_strong, diamond_mine)).
fof(dm_includes_creed, axiom, includes(diamond_mine, creed_brothers)).
fof(dm_includes_ivy, axiom, includes(diamond_mine, ivy_nile)).
fof(imperium_feud_dm, axiom, feud_with(imperium, diamond_mine)).
fof(goal, conjecture, ? [X] : (wrestling_stable(X) & leads(roderick_strong, X))).