% Negative version
fof(p1, axiom, sporting_event(summer_olympic_games)).
fof(p2, axiom, held_in(summer_olympic_games, tokyo)).
fof(p3, axiom, won_most_medals(united_states, tokyo)).
fof(distinct, axiom, (summer_olympic_games != world_championships & summer_olympic_games != tokyo & summer_olympic_games != united_states & world_championships != tokyo & world_championships != united_states & tokyo != united_states)).
fof(goal, conjecture, ~sporting_event(world_championships)).