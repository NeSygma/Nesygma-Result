fof(winner_steinhauer, axiom, winner(steinhauer, dm92)).
fof(participated_steinhauer, axiom, participated(steinhauer, dm92)).
fof(six_way_tie_exists, axiom, ? [X] : (in_six_way_tie(X) & on_leaderboard(X, dm92))).
fof(belgian_in_tie, axiom, ? [X] : (in_six_way_tie(X) & from(X, belgium))).
fof(descampe_belgium, axiom, from(descampe, belgium)).
fof(descampe_leaderboard, axiom, on_leaderboard(descampe, dm92)).
fof(leaderboard_participated, axiom, ! [X] : (on_leaderboard(X, dm92) => participated(X, dm92))).
fof(distinct_names, axiom, (steinhauer != descampe)).
fof(goal, conjecture, winner(steinhauer, dm92)).