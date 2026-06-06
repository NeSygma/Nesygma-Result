% Negative version
fof(p1, axiom, capital_of(beijing, china_prc)).
fof(p2, axiom, capital_of(beijing, most_populous_nation)).
fof(p3, axiom, located_in(beijing, northern_china)).
fof(p4, axiom, hosted(beijing, summer_olympics_2008)).
fof(p5, axiom, hosted(beijing, paralympics_2008_summer)).
fof(p6, axiom, hosted(beijing, summer_olympics)).
fof(p7, axiom, hosted(beijing, winter_olympics)).
fof(p8, axiom, hosted(beijing, summer_paralympics)).
fof(p9, axiom, hosted(beijing, winter_paralympics)).
fof(distinct, axiom, (beijing != china_prc & beijing != most_populous_nation & beijing != northern_china & beijing != summer_olympics_2008 & beijing != winter_olympics & beijing != paralympics_2008_summer & beijing != summer_paralympics_2008 & beijing != summer_olympics & beijing != winter_paralympics & beijing != summer_paralympics & beijing != winter_paralympics)).
fof(goal, conjecture, ~ (hosted(beijing, summer_olympics_2008) & hosted(beijing, winter_olympics))).