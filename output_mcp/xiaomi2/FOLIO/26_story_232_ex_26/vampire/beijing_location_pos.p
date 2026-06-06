fof(premise_capital, axiom, capital_of(beijing, peoples_republic_of_china)).
fof(premise_populous, axiom, capital_city_of(beijing, most_populous_nation)).
fof(premise_northern, axiom, located_in(beijing, northern_china)).
fof(premise_olympics_2008, axiom, hosted(beijing, summer_olympics_2008) & hosted(beijing, summer_paralympics_2008)).
fof(premise_all_games, axiom, hosted(beijing, summer_olympics) & hosted(beijing, winter_olympics) & hosted(beijing, summer_paralympics) & hosted(beijing, winter_paralympics)).
fof(premise_universities, axiom, many_rank_among_best(beijing)).

% Northern and Southern China are mutually exclusive regions
fof(north_south_exclusive, axiom,
    ! [X] : (located_in(X, northern_china) => ~located_in(X, southern_china))).

% Conclusion: Beijing is located in southern China
fof(goal, conjecture, located_in(beijing, southern_china)).