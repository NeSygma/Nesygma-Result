fof(winner_is_steinhauer, axiom, winner(dmc_1992, steinhauer)).
fof(participated_steinhauer, axiom, participated(steinhauer, dmc_1992)).
fof(descampe_on_leaderboard, axiom, on_leaderboard(descampe, dmc_1992)).
fof(descampe_from_belgium, axiom, from_belgium(descampe)).
fof(leaderboard_participated, axiom, ! [X] : (on_leaderboard(X, dmc_1992) => participated(X, dmc_1992))).
fof(goal, conjecture, ~winner(dmc_1992, steinhauer)).