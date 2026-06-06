fof(distinct, axiom, (
    diamond_mine != roderick_strong & diamond_mine != creed_brothers &
    diamond_mine != ivy_nile & diamond_mine != imperium &
    diamond_mine != wwe &
    roderick_strong != creed_brothers & roderick_strong != ivy_nile &
    roderick_strong != imperium & roderick_strong != wwe &
    creed_brothers != ivy_nile & creed_brothers != imperium &
    creed_brothers != wwe &
    ivy_nile != imperium & ivy_nile != wwe &
    imperium != wwe
)).
fof(premise_1, axiom, formed_in(diamond_mine, wwe)).
fof(premise_2, axiom, leads(roderick_strong, diamond_mine)).
fof(premise_3, axiom, includes(diamond_mine, creed_brothers)).
fof(premise_4, axiom, includes(diamond_mine, ivy_nile)).
fof(premise_5, axiom, has_feud_with(imperium, diamond_mine)).
fof(conclusion_neg, conjecture, ~leads(roderick_strong, creed_brothers)).