fof(premise_4, axiom, hosted(beijing, summer_olympics_2008)).
fof(premise_4b, axiom, hosted(beijing, summer_paralympics_2008)).
fof(premise_5, axiom, hosted(beijing, summer_olympics)).
fof(premise_5b, axiom, hosted(beijing, winter_olympics)).
fof(premise_5c, axiom, hosted(beijing, summer_paralympics)).
fof(premise_5d, axiom, hosted(beijing, winter_paralympics)).
fof(summer_olympics_2008_is_summer, axiom,
    ! [X] : (hosted(X, summer_olympics_2008) => hosted(X, summer_olympics))).
fof(goal, conjecture,
    ~(hosted(beijing, summer_olympics_2008) & hosted(beijing, winter_olympics))).