tff(year_type, type, year: $int).
tff(event_type, type, event: $tType).
tff(summer_decl, type, summer: event).
tff(winter_decl, type, winter: event).
tff(beijing_decl, type, beijing: $tType).
tff(prc_decl, type, prc: $tType).

tff(capital_of, axiom, capital_of(beijing, prc)).
tff(capital_of_most_populous, axiom, capital_of_worlds_most_populous(beijing)).
tff(located_in_northern_china, axiom, located_in(beijing, northern_china)).
tff(hosted_2008_summer, axiom, hosted_olympics(beijing, 2008, summer)).
tff(hosted_2008_paralympics, axiom, hosted_paralympics(beijing, 2008, summer)).
tff(hosted_winter, axiom, ? [Y: year] : hosted_olympics(beijing, Y, winter)).

tff(conclusion_negation, conjecture, ~(hosted_olympics(beijing, 2008, summer) & ? [Y: year] : hosted_olympics(beijing, Y, winter))).