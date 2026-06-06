fof(sporting_event_1, axiom, sporting_event(summer_olympic_games)).
fof(location_1, axiom, location(last_summer_olympic_games, tokyo)).
fof(won_most_medals_1, axiom, won_most_medals_in(usa, tokyo)).
fof(rule_won, axiom, ! [E, C, Country] : ((location(E, C) & won_most_medals_in(Country, C)) => won_most_medals_in(Country, E))).
fof(conjecture, conjecture, won_most_medals_in(usa, last_summer_olympic_games)).