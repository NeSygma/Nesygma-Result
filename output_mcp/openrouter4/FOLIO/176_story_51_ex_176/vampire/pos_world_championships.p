fof(premise_1, axiom, sporting_event(summer_olympic_games)).
fof(premise_2, axiom, location(last_summer_olympic_games, tokyo)).
fof(premise_3, axiom, won_most_medals(united_states, tokyo)).
fof(distinct, axiom, (summer_olympic_games != last_summer_olympic_games & summer_olympic_games != tokyo & summer_olympic_games != united_states & summer_olympic_games != world_championships & last_summer_olympic_games != tokyo & last_summer_olympic_games != united_states & last_summer_olympic_games != world_championships & tokyo != united_states & tokyo != world_championships & united_states != world_championships)).
fof(goal, conjecture, sporting_event(world_championships)).