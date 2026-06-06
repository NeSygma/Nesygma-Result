fof(premise1, axiom, capital_of(beijing, prc)).
fof(premise2, axiom, capital_of_worlds_most_populous(beijing)).
fof(premise3, axiom, located_in(beijing, northern_china)).
fof(premise4, axiom, hosted_olympics(beijing, 2008, summer)).
fof(premise5, axiom, hosted_paralympics(beijing, 2008, summer)).
fof(premise6, axiom, ? [Year] : hosted_olympics(beijing, Year, winter)).
fof(conclusion, conjecture, hosted_olympics(beijing, 2008, summer) & ? [Year] : hosted_olympics(beijing, Year, winter)).