tff(year_type, type, year: $tType).
tff(city_type, type, city: $tType).
tff(type_type, type, olympic_type: $tType).
tff(beijing_decl, type, beijing: city).
tff(summer_decl, type, summer: olympic_type).
tff(winter_decl, type, winter: olympic_type).
tff(year_2008_decl, type, year_2008: year).
tff(hosted_olympics_decl, type, hosted_olympics: (city * year * olympic_type) > $o).

tff(premise_1, axiom, hosted_olympics(beijing, year_2008, summer)).
tff(premise_2, axiom, ? [Y: year] : hosted_olympics(beijing, Y, summer)).
tff(premise_3, axiom, ? [Y: year] : hosted_olympics(beijing, Y, winter)).
tff(goal, conjecture, (hosted_olympics(beijing, year_2008, summer) & ? [Y: year] : hosted_olympics(beijing, Y, winter))).