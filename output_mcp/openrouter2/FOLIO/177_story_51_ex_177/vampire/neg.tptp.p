fof(premise1, axiom, sporting_event(summer_olympic_games)).
fof(premise2, axiom, location(last_summer_olympic_games, tokyo)).
fof(premise3, axiom, won_most_medals_in(united_states, tokyo)).
fof(distinct, axiom, (summer_olympic_games != last_summer_olympic_games & summer_olympic_games != tokyo & summer_olympic_games != united_states & last_summer_olympic_games != tokyo & last_summer_olympic_games != united_states & tokyo != united_states)).
fof(conjecture, conjecture, location(last_summer_olympic_games, tokyo)).