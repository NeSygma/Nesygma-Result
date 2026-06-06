fof(winner, axiom, winner_1992(steinhauer)).
fof(participated_steinhauer, axiom, participated_1992(steinhauer)).
fof(six_way_tie_exists, axiom, ? [X] : in_six_way_tie(X)).
fof(belgian_in_tie, axiom, ? [X] : (in_six_way_tie(X) & from_belgium(X))).
fof(descampe_belgian, axiom, from_belgium(descampe)).
fof(descampe_leaderboard, axiom, on_leaderboard_1992(descampe)).
fof(leaderboard_participated, axiom, ! [X] : (on_leaderboard_1992(X) => participated_1992(X))).
fof(goal, conjecture, in_six_way_tie(descampe)).