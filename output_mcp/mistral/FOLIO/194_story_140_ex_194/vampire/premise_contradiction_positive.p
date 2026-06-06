fof(winner_is_steinhauer, axiom, winner(du_maurier_1992, steinhauer)).
fof(six_way_tie_exists, axiom, six_way_tie(du_maurier_1992)).
fof(tie_implies_on_leaderboard, axiom, ! [P] : (in_tie(P, du_maurier_1992) => on_leaderboard(P, du_maurier_1992))).
fof(on_leaderboard_implies_tie, axiom, ! [P] : (on_leaderboard(P, du_maurier_1992) => in_tie(P, du_maurier_1992))).
fof(belgian_in_tie, axiom, ? [P] : (in_tie(P, du_maurier_1992) & from_belgium(P))).
fof(descampe_belgian, axiom, from_belgium(descampe)).
fof(descampe_on_leaderboard, axiom, on_leaderboard(descampe, du_maurier_1992)).
fof(conclusion, conjecture, ~winner(du_maurier_1992, steinhauer)).