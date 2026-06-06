% Negative file: negated conclusion as conjecture
% Negated conclusion: Steinhauer WAS the winner
% So conjecture: winner(steinhauer)

fof(distinct, axiom, (steinhauer != descampe)).

fof(premise_1, axiom, winner(steinhauer)).
fof(premise_2, axiom, participated(steinhauer)).
fof(premise_3, axiom, ? [X] : (six_way_tie(X) & from_belgium(X))).
fof(premise_4, axiom, (from_belgium(descampe) & on_leaderboard(descampe))).
fof(premise_5, axiom, ! [X] : (on_leaderboard(X) => participated(X))).

fof(goal, conjecture, winner(steinhauer)).