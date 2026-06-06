fof(stable_diamond_mine, axiom, stable(diamond_mine)).
fof(formed_in_diamond_mine, axiom, formed_in(diamond_mine, wwe)).
fof(leads_roderick, axiom, leads(roderick_strong, diamond_mine)).
fof(includes_creed, axiom, includes(diamond_mine, creed_brothers)).
fof(includes_ivy, axiom, includes(diamond_mine, ivy_nile)).
fof(feud_imperium, axiom, feud_with(imperium, diamond_mine)).
fof(distinct, axiom, (diamond_mine != wwe & diamond_mine != roderick_strong & diamond_mine != creed_brothers & diamond_mine != ivy_nile & diamond_mine != imperium & wwe != roderick_strong & wwe != creed_brothers & wwe != ivy_nile & wwe != imperium & roderick_strong != creed_brothers & roderick_strong != ivy_nile & roderick_strong != imperium & creed_brothers != ivy_nile & creed_brothers != imperium & ivy_nile != imperium)).
fof(conjecture, conjecture, leads(roderick_strong, creed_brothers)).