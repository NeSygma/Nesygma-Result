% Axioms
fof(axiom_1, axiom, capital(beijing, china)).
fof(axiom_2, axiom, capital(beijing, most_populous_nation)).
fof(axiom_3, axiom, located_in(beijing, northern_china)).
fof(axiom_4, axiom, hosted(beijing, summer_olympics_2008)).
fof(axiom_5, axiom, hosted(beijing, summer_paralympics_2008)).
fof(axiom_6, axiom, hosted(beijing, summer_olympics)).
fof(axiom_7, axiom, hosted(beijing, winter_olympics)).
fof(axiom_8, axiom, hosted(beijing, summer_paralympics)).
fof(axiom_9, axiom, hosted(beijing, winter_paralympics)).
% Conjecture
fof(conjecture, conjecture, (hosted(beijing, summer_olympics_2008) & hosted(beijing, winter_olympics))).