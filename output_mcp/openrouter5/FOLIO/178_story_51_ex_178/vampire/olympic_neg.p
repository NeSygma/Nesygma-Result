% Negative version: negated conclusion as conjecture
fof(premise_1, axiom, summer_olympic_games(summer_olympic_games_event)).
fof(premise_2, axiom, last_summer_olympic_games(tokyo)).
fof(premise_3, axiom, most_medals(united_states, tokyo)).
fof(goal_neg, conjecture, ~most_medals(united_states, last_summer_olympic_games)).