fof(beijing_capital_china, axiom, capital_of(beijing, china)).
fof(beijing_capital_populous, axiom, capital_of(beijing, most_populous_nation)).
fof(beijing_northern, axiom, located_in(beijing, northern_china)).
fof(beijing_summer_olympics_2008, axiom, hosted(beijing, summer_olympics_2008)).
fof(beijing_summer_paralympics_2008, axiom, hosted(beijing, summer_paralympics_2008)).
fof(beijing_summer_olympics, axiom, hosted(beijing, summer_olympics)).
fof(beijing_winter_olympics, axiom, hosted(beijing, winter_olympics)).
fof(beijing_summer_paralympics, axiom, hosted(beijing, summer_paralympics)).
fof(beijing_winter_paralympics, axiom, hosted(beijing, winter_paralympics)).
fof(northern_southern_distinct, axiom, northern_china != southern_china).
fof(northern_not_southern, axiom, ! [X] : (located_in(X, northern_china) => ~located_in(X, southern_china))).
fof(goal, conjecture, ~located_in(beijing, southern_china)).