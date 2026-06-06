fof(beijing_is_capital_of_prc, axiom, capital_of(beijing, prc)).
fof(beijing_is_capital_of_most_populous, axiom, capital_of_worlds_most_populous(beijing)).
fof(beijing_in_northern_china, axiom, located_in(beijing, northern_china)).
fof(beijing_hosted_2008_summer_olympics, axiom, hosted(beijing, summer_olympics, year_2008)).
fof(beijing_hosted_2008_summer_paralympics, axiom, hosted(beijing, summer_paralympics, year_2008)).
fof(beijing_hosted_winter_olympics, axiom, ? [Y] : hosted(beijing, winter_olympics, Y)).
fof(distinct_entities, axiom, beijing != prc & beijing != northern_china & prc != northern_china & summer_olympics != winter_olympics & summer_paralympics != winter_paralympics).
fof(conclusion_negation, conjecture, ~(hosted(beijing, summer_olympics, year_2008) & ? [Y] : hosted(beijing, winter_olympics, Y))).