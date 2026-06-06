fof(axiom_1, axiom, winner(steinhauer, du_maurier_classic_1992)).
fof(axiom_2, axiom, participated(steinhauer, du_maurier_classic_1992)).
fof(axiom_3, axiom, ? [X] : (six_way_tie(X) & from_belgium(X) & on_leaderboard(X, du_maurier_classic_1992))).
fof(axiom_4, axiom, from_belgium(descampes)).
fof(axiom_5, axiom, on_leaderboard(descampes, du_maurier_classic_1992)).
fof(axiom_6, axiom, ! [X] : (on_leaderboard(X, du_maurier_classic_1992) => participated(X, du_maurier_classic_1992))).
fof(conjecture, conjecture, winner(steinhauer, du_maurier_classic_1992)).