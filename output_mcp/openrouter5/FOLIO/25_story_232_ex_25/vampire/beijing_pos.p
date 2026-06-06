% Positive version: original claim as conjecture
% Premises
fof(premise_1, axiom, capital_of(beijing, people_republic_of_china)).
fof(premise_2, axiom, capital_city_of(beijing, worlds_most_populous_nation)).
fof(premise_3, axiom, located_in(beijing, northern_china)).
fof(premise_4, axiom, hosted(beijing, olympics_2008_summer)).
fof(premise_5, axiom, hosted(beijing, paralympics_2008_summer)).
fof(premise_6, axiom, hosted(beijing, olympics_summer)).
fof(premise_7, axiom, hosted(beijing, olympics_winter)).
fof(premise_8, axiom, hosted(beijing, paralympics_summer)).
fof(premise_9, axiom, hosted(beijing, paralympics_winter)).
fof(premise_10, axiom, many_universities_rank_among_best(beijing)).

% Conclusion to evaluate: Beijing hosted both the 2008 Summer Olympics and the Winter Olympics.
fof(goal, conjecture, (hosted(beijing, olympics_2008_summer) & hosted(beijing, olympics_winter))).