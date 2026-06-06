tff(person_type, type, person: $tType).
tff(group_type, type, group: $tType).
tff(stable_type, type, stable: $tType).

tff(diamond_mine_decl, type, diamond_mine: stable).
tff(roderick_strong_decl, type, roderick_strong: person).
tff(creed_brothers_decl, type, creed_brothers: group).
tff(ivy_nile_decl, type, ivy_nile: person).
tff(imperium_decl, type, imperium: group).

tff(leads_pred, type, leads: (person * stable) > $o).
tff(includes_pred, type, includes: (stable * group) > $o).
tff(has_feud_pred, type, has_feud: (group * group) > $o).

tff(premise1, axiom, leads(roderick_strong, diamond_mine)).
tff(premise2, axiom, includes(diamond_mine, creed_brothers)).
tff(premise3, axiom, includes(diamond_mine, ivy_nile)).
tff(premise4, axiom, has_feud(imperium, diamond_mine)).

tff(conclusion_negation, conjecture, ~leads(roderick_strong, diamond_mine)).