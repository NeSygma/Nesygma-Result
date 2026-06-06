fof(premise1, axiom, sporting_event(summer_olympic_games)).
fof(premise2, axiom, held_in(last_summer_olympic_games, tokyo)).
fof(premise3, axiom, won_most_medals_in(usa, tokyo)).
fof(distinct_constants, axiom, (last_summer_olympic_games != tokyo & last_summer_olympic_games != usa & tokyo != usa)).
fof(neg_conjecture, conjecture, ~won_most_medals_in(usa, last_summer_olympic_games)).