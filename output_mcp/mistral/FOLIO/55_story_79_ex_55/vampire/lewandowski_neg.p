fof(premise1, axiom, striker(robert_lewandowski)).
fof(premise2, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(premise3, axiom, left_team(robert_lewandowski, bayern_munchen)).
fof(premise4, axiom, ! [P, T] : (left_team(P, T) => ~plays_for(P, T))).
fof(distinct_entities, axiom, robert_lewandowski != bayern_munchen).
fof(conclusion_negation, conjecture, ~soccer_player(robert_lewandowski)).