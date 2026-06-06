fof(premise1, axiom, capital_of(beijing, prc)).
fof(premise2, axiom, capital_of_worlds_most_populous_nation(beijing)).
fof(premise3, axiom, located_in(beijing, northern_china)).
fof(premise4a, axiom, hosted_olympics(beijing, year_2008, summer)).
fof(premise4b, axiom, hosted_paralympics(beijing, year_2008, summer)).
fof(premise5, axiom, has_hosted_all_olympic_types(beijing)).
fof(premise6, axiom, many_universities_rank_high(beijing, 91)).

fof(has_hosted_all_olympic_types_def, axiom,
    ! [City] : (has_hosted_all_olympic_types(City) <=>
               ( ? [Year] : hosted_olympics(City, Year, summer) &
                 ? [Year] : hosted_olympics(City, Year, winter) ))).

fof(conclusion, conjecture,
    hosted_olympics(beijing, year_2008, summer) &
    ? [Year] : hosted_olympics(beijing, Year, winter)).