fof(fact_loc_north, axiom, located_in(beijing, northern_china)).
fof(excl, axiom, ~ (located_in(beijing, northern_china) & located_in(beijing, southern_china))).
fof(distinct, axiom, (beijing != northern_china & beijing != southern_china & northern_china != southern_china)).
fof(goal, conjecture, located_in(beijing, southern_china)).