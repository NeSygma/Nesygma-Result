fof(winner_is_steinhauer, axiom, winner_of_1992_du_maurier(steinhauer)).
fof(steinhauer_participated, axiom, participated_in_1992_du_maurier(steinhauer)).
fof(six_way_tie_exists, axiom, six_way_tie).
fof(belgian_in_leaderboard, axiom, ? [X] : (leaderboard_1992_du_maurier(X) & from_belgium(X))).
fof(descampe_from_belgium, axiom, from_belgium(descampe)).
fof(descampe_on_leaderboard, axiom, leaderboard_1992_du_maurier(descampe)).
fof(all_leaderboard_participated, axiom, ! [X] : (leaderboard_1992_du_maurier(X) => participated_in_1992_du_maurier(X))).
fof(distinct_people, axiom, steinhauer != descampe).
fof(conclusion, conjecture, ~winner_of_1992_du_maurier(steinhauer)).