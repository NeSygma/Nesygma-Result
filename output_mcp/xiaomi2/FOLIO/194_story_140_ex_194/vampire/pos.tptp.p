fof(winner_steinhauer, axiom, winner(steinhauer)).
fof(participated_steinhauer, axiom, participated(steinhauer)).
fof(six_way_tie, axiom, ? [X] : (in_six_way_tie(X) & on_leaderboard(X) & from_belgium(X))).
fof(descampe_belgium_leaderboard, axiom, (from_belgium(descampe) & on_leaderboard(descampe))).
fof(leaderboard_participated, axiom, ! [X] : (on_leaderboard(X) => participated(X))).
fof(distinct_names, axiom, steinhauer != descampe).
fof(goal, conjecture, ~winner(steinhauer)).