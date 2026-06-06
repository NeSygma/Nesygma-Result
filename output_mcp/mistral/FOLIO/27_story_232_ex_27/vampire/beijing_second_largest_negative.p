fof(prc_is_china, axiom, prc = china).
fof(china_is_world_most_populous, axiom, world_most_populous_nation = china).
fof(premise_1, axiom, capital_of(beijing, prc)).
fof(premise_2, axiom, capital_city_of(beijing, world_most_populous_nation)).
fof(premise_3, axiom, located_in(beijing, northern_china)).
fof(premise_4, axiom, hosted(beijing, summer_olympics_2008)).
fof(premise_5, axiom, hosted(beijing, summer_paralympics_2008)).
fof(premise_6, axiom, has_hosted(beijing, summer_winter_olympics)).
fof(premise_7, axiom, has_hosted(beijing, summer_winter_paralympics)).
fof(premise_8, axiom, ? [U] : (university_in_city(U, beijing) & ranks_among_best_universities(U))).
fof(conclusion_negation, conjecture, ~second_largest_city(beijing, china)).