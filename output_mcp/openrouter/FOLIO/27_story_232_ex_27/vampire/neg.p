% Negative test: conjecture that Beijing is NOT second largest Chinese city
fof(beijing_const, axiom, beijing = beijing).
fof(china_const, axiom, china = china).
fof(world_const, axiom, world = world).
% Premises
fof(p1, axiom, capital_of(beijing, china)).
fof(p2, axiom, capital_city_of(beijing, china)).
fof(p3, axiom, located_in(beijing, northern_china)).
fof(p4, axiom, hosted(beijing, olympics_2008_summer)).
fof(p5, axiom, hosted(beijing, paralympics_2008_summer)).
fof(p6, axiom, hosted(beijing, olympics_summer)).
fof(p7, axiom, hosted(beijing, olympics_winter)).
fof(p8, axiom, hosted(beijing, paralympics_summer)).
fof(p9, axiom, hosted(beijing, paralympics_winter)).
fof(p10, axiom, many_universities_rank_high(beijing)).
% Negated conjecture
fof(goal, conjecture, ~second_largest_city_in_china(beijing)).