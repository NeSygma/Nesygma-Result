fof(striker_fact, axiom, striker(robert_lewandowski)).
fof(striker_to_player, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(left_team_fact, axiom, left_team(robert_lewandowski, bayern_munchen)).
fof(left_team_rule, axiom, ! [X, Y] : (left_team(X, Y) => ~plays_for(X, Y))).
fof(goal, conjecture, plays_for(robert_lewandowski, bayern_munchen)).