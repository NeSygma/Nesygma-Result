fof(dm_is_stable, axiom, professional_wrestling_stable(diamond_mine)).
fof(dm_formed_wwe, axiom, formed_in_wwe(diamond_mine)).
fof(roderick_leads_dm, axiom, leads(roderick_strong, diamond_mine)).
fof(dm_includes_creeds, axiom, includes(diamond_mine, creed_brothers)).
fof(dm_includes_ivy, axiom, includes(diamond_mine, ivy_nile)).
fof(imperium_feud_dm, axiom, has_feud_with(imperium, diamond_mine)).

fof(goal, conjecture, ~? [X] : (professional_wrestling_stable(X) & includes(X, ivy_nile) & has_feud_with(imperium, X))).