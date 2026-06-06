fof(axiom_1, axiom, professional_wrestling_stable(diamond_mine)).
fof(axiom_2, axiom, leads(roderick_strong, diamond_mine)).
fof(axiom_3, axiom, includes(diamond_mine, creed_brothers)).
fof(axiom_4, axiom, includes(diamond_mine, ivy_nile)).
fof(axiom_5, axiom, feud(imperium, diamond_mine)).
fof(distinct_1, axiom, (diamond_mine != roderick_strong)).
fof(distinct_2, axiom, (diamond_mine != creed_brothers)).
fof(distinct_3, axiom, (diamond_mine != ivy_nile)).
fof(distinct_4, axiom, (diamond_mine != imperium)).
fof(distinct_5, axiom, (roderick_strong != creed_brothers)).
fof(distinct_6, axiom, (roderick_strong != ivy_nile)).
fof(distinct_7, axiom, (roderick_strong != imperium)).
fof(distinct_8, axiom, (creed_brothers != ivy_nile)).
fof(distinct_9, axiom, (creed_brothers != imperium)).
fof(distinct_10, axiom, (ivy_nile != imperium)).
fof(conjecture, conjecture, ! [X] : (professional_wrestling_stable(X) & includes(X, ivy_nile) => ~feud(imperium, X))).