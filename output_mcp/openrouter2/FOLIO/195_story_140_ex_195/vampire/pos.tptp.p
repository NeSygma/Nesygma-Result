fof(winner_fact, axiom, winner(du_maurier_1992, steinhauer)).
fof(participated_winner, axiom, participated(du_maurier_1992, steinhauer)).
fof(participated_descampe, axiom, participated(du_maurier_1992, descampe)).
fof(on_leaderboard_descampe, axiom, on_leaderboard(du_maurier_1992, descampe)).
fof(from_country_descampe, axiom, from_country(descampe, belgium)).
fof(on_leaderboard_implies_participated, axiom, ! [X] : (on_leaderboard(du_maurier_1992, X) => participated(du_maurier_1992, X))).
fof(distinct_people, axiom, steinhauer != descampe).
fof(tie_group_exists, axiom,
    ? [P1,P2,P3,P4,P5,P6] :
    (P1 != P2 & P1 != P3 & P1 != P4 & P1 != P5 & P1 != P6 &
     P2 != P3 & P2 != P4 & P2 != P5 & P2 != P6 &
     P3 != P4 & P3 != P5 & P3 != P6 &
     P4 != P5 & P4 != P6 &
     P5 != P6 &
     on_leaderboard(du_maurier_1992, P1) & on_leaderboard(du_maurier_1992, P2) & on_leaderboard(du_maurier_1992, P3) & on_leaderboard(du_maurier_1992, P4) & on_leaderboard(du_maurier_1992, P5) & on_leaderboard(du_maurier_1992, P6) &
     tie(du_maurier_1992, P1) & tie(du_maurier_1992, P2) & tie(du_maurier_1992, P3) & tie(du_maurier_1992, P4) & tie(du_maurier_1992, P5) & tie(du_maurier_1992, P6))) .
fof(belgium_in_tie_exists, axiom,
    ? [Q] : (tie(du_maurier_1992, Q) & from_country(Q, belgium))).
fof(goal, conjecture, tie(du_maurier_1992, descampe)).