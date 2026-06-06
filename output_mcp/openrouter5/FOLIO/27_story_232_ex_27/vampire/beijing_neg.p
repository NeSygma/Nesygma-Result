% Negative version: negated claim as conjecture
% Premises - using only unary/binary predicates, no integer constants in fof
fof(premise_1, axiom, capital_of(beijing, people_republic_of_china)).
fof(premise_2, axiom, capital_city_of_most_populous_nation(beijing)).
fof(premise_3, axiom, located_in(beijing, northern_china)).
fof(premise_4, axiom, hosted(beijing, olympics_2008_summer)).
fof(premise_5, axiom, hosted(beijing, paralympics_2008_summer)).
fof(premise_6, axiom, hosted(beijing, olympics_summer)).
fof(premise_7, axiom, hosted(beijing, olympics_winter)).
fof(premise_8, axiom, hosted(beijing, paralympics_summer)).
fof(premise_9, axiom, hosted(beijing, paralympics_winter)).
fof(premise_10, axiom, has_many_universities(beijing)).
fof(premise_11, axiom, universities_rank_among_best(beijing)).

% Negated conclusion: Beijing is NOT the second largest Chinese city
fof(conclusion_neg, conjecture, ~second_largest_chinese_city(beijing)).