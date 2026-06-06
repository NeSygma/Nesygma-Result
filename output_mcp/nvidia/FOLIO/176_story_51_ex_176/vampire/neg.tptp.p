% Axioms
fof(axiom_1, axiom, sporting_event(last_summer_olympic_games)).
fof(axiom_2, axiom, held_in(last_summer_olympic_games, tokyo)).
fof(axiom_3, axiom, won_most_medals(united_states, tokyo)).
fof(distinct_constants, axiom, (last_summer_olympic_games != tokyo & last_summer_olympic_games != united_states & last_summer_olympic_games != world_championships & tokyo != united_states & tokyo != world_championships & united_states != world_championships)).
fof(conjecture, conjecture, ~sporting_event(world_championships)).