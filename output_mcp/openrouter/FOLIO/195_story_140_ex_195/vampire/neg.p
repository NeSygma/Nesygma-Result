% Negative version
fof(p1, axiom, winner(steinhauer)).
fof(p2, axiom, participated(steinhauer)).
fof(p3, axiom, on_leaderboard(descampe)).
fof(p4, axiom, from_belgium(descampe)).
fof(p5, axiom, ! [X] : (on_leaderboard(X) => participated(X))).
fof(p6, axiom, ? [X] : (in_six_way_tie(X) & from_belgium(X))).
fof(distinct, axiom, steinhauer != descampe).
fof(goal, conjecture, ~in_six_way_tie(descampe)).