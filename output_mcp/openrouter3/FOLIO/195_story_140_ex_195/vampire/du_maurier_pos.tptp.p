% Positive version: Descampe is in the six-way tie
fof(winner_is_steinhauer, axiom, winner_of(du_maurier_1992, steinhauer)).
fof(steinhauer_participated, axiom, participated_in(du_maurier_1992, steinhauer)).
fof(six_way_tie_exists, axiom, ? [P1,P2,P3,P4,P5,P6] : (
    in_tie(P1, du_maurier_1992) & in_tie(P2, du_maurier_1992) & 
    in_tie(P3, du_maurier_1992) & in_tie(P4, du_maurier_1992) & 
    in_tie(P5, du_maurier_1992) & in_tie(P6, du_maurier_1992) &
    P1 != P2 & P1 != P3 & P1 != P4 & P1 != P5 & P1 != P6 &
    P2 != P3 & P2 != P4 & P2 != P5 & P2 != P6 &
    P3 != P4 & P3 != P5 & P3 != P6 &
    P4 != P5 & P4 != P6 &
    P5 != P6 &
    from_country(P1, belgium)
)).
fof(descampe_from_belgium, axiom, from_country(descampe, belgium)).
fof(descampe_on_leaderboard, axiom, on_leaderboard(du_maurier_1992, descampe)).
fof(leaderboard_participation, axiom, 
    ! [P] : (on_leaderboard(du_maurier_1992, P) => participated_in(du_maurier_1992, P))).
fof(goal, conjecture, in_tie(descampe, du_maurier_1992)).