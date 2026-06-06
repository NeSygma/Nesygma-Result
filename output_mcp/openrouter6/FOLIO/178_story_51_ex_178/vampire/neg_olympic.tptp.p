fof(premise1, axiom, sporting_event(summer_olympic_games_type)).
fof(premise2, axiom, host_city(last_summer_olympic_games, tokyo)).
fof(premise3, axiom, won_most_medals(united_states, tokyo_olympics)).
fof(same_event, axiom, last_summer_olympic_games = tokyo_olympics).
fof(distinct1, axiom, tokyo != united_states).
fof(distinct2, axiom, tokyo != summer_olympic_games_type).
fof(distinct3, axiom, united_states != summer_olympic_games_type).
fof(goal, conjecture, ~won_most_medals(united_states, last_summer_olympic_games)).