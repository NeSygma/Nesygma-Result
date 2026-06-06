% Positive file: original conclusion as conjecture
% Premises
fof(premise_1, axiom, capital_of(beijing, people_republic_of_china)).
fof(premise_2, axiom, capital_city_of_most_populous_nation(beijing)).
fof(premise_3, axiom, located_in(beijing, northern_china)).
fof(premise_4, axiom, hosted_summer_olympics_paralympics_2008(beijing)).
fof(premise_5, axiom, hosted_summer_winter_olympics_paralympics(beijing)).
fof(premise_6, axiom, has_top_universities(beijing)).

% Conclusion: Beijing is located in southern China.
fof(goal, conjecture, located_in(beijing, southern_china)).