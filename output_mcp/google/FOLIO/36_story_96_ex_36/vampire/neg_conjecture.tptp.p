fof(stable_def, axiom, is_stable(diamond_mine)).
fof(leader_def, axiom, leads(roderick_strong, diamond_mine)).
fof(includes_creed, axiom, includes(diamond_mine, creed_brothers)).
fof(includes_ivy, axiom, includes(diamond_mine, ivy_nile)).
fof(feud_def, axiom, has_feud(imperium, diamond_mine)).
fof(goal, conjecture, ? [S] : (is_stable(S) & includes(S, ivy_nile) & has_feud(imperium, S))).