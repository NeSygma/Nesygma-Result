fof(p1, axiom, winner(steinhauer, du_maurier_1992)).
fof(p2, axiom, participated(steinhauer, du_maurier_1992)).
fof(p3, axiom, six_way_tie_on_leaderboard(du_maurier_1992)).
fof(p4, axiom, ? [X] : (in_six_way_tie(X, du_maurier_1992) & from_belgium(X))).
fof(p5, axiom, from_belgium(descampe)).
fof(p6, axiom, on_leaderboard(descampe, du_maurier_1992)).
fof(p7, axiom, ! [X] : (on_leaderboard(X, du_maurier_1992) => participated(X, du_maurier_1992))).
fof(goal, conjecture, in_six_way_tie(descampe, du_maurier_1992)).