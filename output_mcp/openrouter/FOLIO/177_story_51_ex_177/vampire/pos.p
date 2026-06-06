% Positive test: conclusion that last games were not in Tokyo
fof(premise1, axiom, sporting_event(last_summer_olympic_games)).
fof(premise2, axiom, in_city(last_summer_olympic_games, tokyo)).
fof(premise3, axiom, won_most_medals(united_states, tokyo)).
% distinctness of constants
fof(distinct1, axiom, (last_summer_olympic_games != tokyo & united_states != tokyo & united_states != last_summer_olympic_games)).
fof(goal, conjecture, ~in_city(last_summer_olympic_games, tokyo)).