% Negative: negated claim as conjecture
fof(distinct, axiom, steinhauer != descampe).

fof(premise_1, axiom, winner(steinhauer)).
fof(premise_2, axiom, participated(steinhauer)).
fof(premise_3a, axiom, ? [X] : in_six_way_tie(X)).
fof(premise_3b, axiom, ! [X] : (in_six_way_tie(X) => on_leaderboard(X))).
fof(premise_3c, axiom, ? [X] : (in_six_way_tie(X) & from_belgium(X))).
fof(premise_4, axiom, from_belgium(descampe) & on_leaderboard(descampe)).
fof(premise_5, axiom, ! [X] : (on_leaderboard(X) => participated(X))).

fof(neg_conclusion, conjecture, winner(steinhauer)).