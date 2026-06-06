fof(winner, axiom, winner_of(dm_1992, steinhauer)).
fof(participated_steinhauer, axiom, participated_in(dm_1992, steinhauer)).
fof(six_way_tie_belgian, axiom, ? [X] : (six_way_tie(dm_1992, X) & from_belgium(X))).
fof(descampe_belgian, axiom, from_belgium(descampe)).
fof(descampe_leaderboard, axiom, on_leaderboard(dm_1992, descampe)).
fof(all_participated, axiom, ! [P] : (on_leaderboard(dm_1992, P) => participated_in(dm_1992, P))).

fof(conclusion_negation, conjecture, ~six_way_tie(dm_1992, descampe)).