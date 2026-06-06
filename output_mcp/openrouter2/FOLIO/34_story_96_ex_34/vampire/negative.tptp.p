fof(stable_diamond_mine, axiom, stable(diamond_mine)).
fof(leads_rstrong_diamond_mine, axiom, leads(rstrong, diamond_mine)).
fof(member_creed_brothers, axiom, member_of(creed_brothers, diamond_mine)).
fof(member_ivy_nile, axiom, member_of(ivy_nile, diamond_mine)).
fof(feud_imperium, axiom, feud(imperium, diamond_mine)).
fof(distinctness, axiom, (rstrong != diamond_mine & rstrong != creed_brothers & rstrong != ivy_nile & rstrong != imperium & diamond_mine != creed_brothers & diamond_mine != ivy_nile & diamond_mine != imperium & creed_brothers != ivy_nile & creed_brothers != imperium & ivy_nile != imperium)).
fof(conjecture, conjecture, ~? [Y] : (leads(rstrong, Y) & stable(Y))).