fof(premise1, axiom, is_sporting_event(summer_olympic_games)).
fof(premise2, axiom, last_held_in(summer_olympic_games, tokyo)).
fof(premise3, axiom, won_most_medals(united_states, tokyo)).
fof(distinct_entities, axiom, (summer_olympic_games != tokyo & summer_olympic_games != united_states & tokyo != united_states)).
fof(conclusion, conjecture, won_most_medals(united_states, summer_olympic_games)).