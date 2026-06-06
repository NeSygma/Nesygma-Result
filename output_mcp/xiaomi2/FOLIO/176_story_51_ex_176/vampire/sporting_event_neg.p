fof(premise_1, axiom, sporting_event(summer_olympics)).
fof(premise_2, axiom, last_summer_olympics_in(tokyo)).
fof(premise_3, axiom, won_most_medals_in(united_states, tokyo)).
fof(distinct, axiom, (summer_olympics != world_championships & summer_olympics != tokyo & summer_olympics != united_states & world_championships != tokyo & world_championships != united_states & tokyo != united_states)).
fof(goal, conjecture, ~sporting_event(world_championships)).