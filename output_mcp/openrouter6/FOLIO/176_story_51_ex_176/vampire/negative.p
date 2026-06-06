fof(axiom1, axiom, sporting_event(summer_olympic_games)).
fof(axiom2, axiom, location(summer_olympic_games, tokyo)).
fof(axiom3, axiom, won_most_medals(united_states, tokyo)).
fof(distinct, axiom, (summer_olympic_games != tokyo & summer_olympic_games != united_states & summer_olympic_games != world_championships & tokyo != united_states & tokyo != world_championships & united_states != world_championships)).
fof(goal, conjecture, ~sporting_event(world_championships)).