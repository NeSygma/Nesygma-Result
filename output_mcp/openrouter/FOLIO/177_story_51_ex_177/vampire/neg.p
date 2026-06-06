% Negative test: negation of the conclusion (i.e., that the last games were in Tokyo)
fof(premise1, axiom, sporting_event(last_summer_olympic_games)).
fof(premise2, axiom, in_city(last_summer_olympic_games, tokyo)).
fof(premise3, axiom, won_most_medals(united_states, tokyo)).
fof(distinct1, axiom, (last_summer_olympic_games != tokyo & united_states != tokyo & united_states != last_summer_olympic_games)).
fof(goal, conjecture, in_city(last_summer_olympic_games, tokyo)).