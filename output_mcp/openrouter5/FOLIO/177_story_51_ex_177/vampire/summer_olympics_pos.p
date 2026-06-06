% Positive file: original conclusion as conjecture
% Premises:
fof(premise1, axiom, summer_olympic_games_event).
fof(premise2, axiom, last_summer_olympic_games(tokyo)).
fof(premise3, axiom, most_medals_won(usa, tokyo)).

% Conclusion to evaluate: The last summer Olympic games were not in Tokyo.
fof(goal, conjecture, ~last_summer_olympic_games(tokyo)).