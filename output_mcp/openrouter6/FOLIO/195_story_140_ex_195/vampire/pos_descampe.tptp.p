% Positive: Descampe is in the six-way tie
fof(event_decl, axiom, e1992 = event_1992_du_maurier).
fof(person_decl, axiom, (steinhauer != descampe)).
fof(winner, axiom, winner(e1992, steinhauer)).
fof(part_steinhauer, axiom, participated(e1992, steinhauer)).
fof(six_way_tie_exists, axiom, ? [P] : (in_six_way_tie(P, e1992) & from_country(P, belgium))).
fof(descampe_from_belgium, axiom, from_country(descampe, belgium)).
fof(descampe_on_leaderboard, axiom, on_leaderboard(e1992, descampe)).
fof(all_on_leaderboard_participated, axiom, ! [X] : (on_leaderboard(e1992, X) => participated(e1992, X))).
fof(goal, conjecture, in_six_way_tie(descampe, e1992)).