fof(premise1, axiom, sporting_event(summer_olympic_games)).
fof(premise2, axiom, location_of_event(summer_olympic_games, tokyo)).
fof(premise3, axiom, won_most_medals(united_states, tokyo)).
fof(distinct, axiom, (summer_olympic_games != world_championships & summer_olympic_games != tokyo & summer_olympic_games != united_states & world_championships != tokyo & world_championships != united_states & tokyo != united_states)).
fof(conjecture, conjecture, sporting_event(world_championships)).