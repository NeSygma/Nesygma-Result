fof(diamond_mine_formed, axiom, stable(diamond_mine)).
fof(roderick_leads_diamond_mine, axiom, leads(roderick_strong, diamond_mine)).
fof(diamond_mine_includes_creed, axiom, includes(diamond_mine, creed_brothers)).
fof(diamond_mine_includes_nile, axiom, includes(diamond_mine, ivy_nile)).
fof(imperium_feuds_diamond_mine, axiom, feuds(imperium, diamond_mine)).
fof(distinct_entities, axiom, roderick_strong != diamond_mine & roderick_strong != creed_brothers & roderick_strong != ivy_nile & roderick_strong != imperium & diamond_mine != creed_brothers & diamond_mine != ivy_nile & diamond_mine != imperium & creed_brothers != ivy_nile & creed_brothers != imperium & ivy_nile != imperium).
fof(conclusion_negation, conjecture, ~leads(roderick_strong, creed_brothers)).