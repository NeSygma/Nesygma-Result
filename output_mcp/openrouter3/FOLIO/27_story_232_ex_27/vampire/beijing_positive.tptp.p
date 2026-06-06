% Beijing Capital Problem - Positive Version
% Premises about Beijing
fof(premise_1, axiom, capital_of(beijing, china)).
fof(premise_2, axiom, most_populous_nation(china)).
fof(premise_3, axiom, located_in(beijing, northern_china)).
fof(premise_4, axiom, hosted_event(beijing, summer_olympics_2008)).
fof(premise_5, axiom, hosted_event(beijing, summer_paralympics_2008)).
fof(premise_6, axiom, hosted_event(beijing, summer_olympics)).
fof(premise_7, axiom, hosted_event(beijing, winter_olympics)).
fof(premise_8, axiom, hosted_event(beijing, summer_paralympics)).
fof(premise_9, axiom, hosted_event(beijing, winter_paralympics)).
fof(premise_10, axiom, has_universities(beijing, 91)).

% Distinctness axioms (Beijing is a unique city)
fof(distinct_cities, axiom, (beijing != shanghai & beijing != guangzhou & beijing != shenzhen)).

% Conclusion to evaluate
fof(goal, conjecture, second_largest_city(beijing)).