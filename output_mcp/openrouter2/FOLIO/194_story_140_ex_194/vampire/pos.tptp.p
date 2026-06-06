fof(premise1, axiom, winner(steinhauer, du_maurier_1992)).
fof(premise2, axiom, participated(steinhauer, du_maurier_1992)).
fof(premise3, axiom, from_country(descampe, belgium)).
fof(premise4, axiom, on_leaderboard(descampe, du_maurier_1992)).
fof(premise5, axiom, ! [X] : (on_leaderboard(X, du_maurier_1992) => participated(X, du_maurier_1992))).
fof(distinct, axiom, steinhauer != descampe).
fof(conjecture, conjecture, ~winner(steinhauer, du_maurier_1992)).