% Negative conjecture: There exists a stable that includes Ivy Nile and Imperium has a feud with it.
fof(distinct_names, axiom, (diamond_mine != imperium & diamond_mine != roderick_strong & diamond_mine != creed_brothers & diamond_mine != ivy_nile & imperium != roderick_strong & imperium != creed_brothers & imperium != ivy_nile & roderick_strong != creed_brothers & roderick_strong != ivy_nile & creed_brothers != ivy_nile)).
fof(stable_diamond, axiom, stable(diamond_mine)).
fof(lead_rod, axiom, leads(roderick_strong, diamond_mine)).
fof(includes_creed, axiom, includes(diamond_mine, creed_brothers)).
fof(includes_ivy, axiom, includes(diamond_mine, ivy_nile)).
fof(feud_imperium_diamond, axiom, feud(imperium, diamond_mine)).
fof(goal_neg, conjecture, ? [S] : (stable(S) & includes(S, ivy_nile) & feud(imperium, S))).