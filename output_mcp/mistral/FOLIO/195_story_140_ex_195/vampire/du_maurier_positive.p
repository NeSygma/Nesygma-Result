fof(winner_is_steinhauer, axiom, winner_of(du_maurier_1992, steinhauer)).
fof(steinhauer_participated, axiom, participated_in(steinhauer, du_maurier_1992)).
fof(belgian_in_six_way_tie_exists, axiom, ? [P] : (six_way_tie_member(P, du_maurier_1992) & from_belgium(P))).
fof(descampe_belgian_and_on_leaderboard, axiom, from_belgium(descampe) & leaderboard_member(descampe, du_maurier_1992)).
fof(all_leaderboard_members_participated, axiom, ! [P] : (leaderboard_member(P, du_maurier_1992) => participated_in(P, du_maurier_1992))).
fof(six_way_tie_members_are_leaderboard_members, axiom, ! [P] : (six_way_tie_member(P, du_maurier_1992) => leaderboard_member(P, du_maurier_1992))).
fof(exactly_six_in_tie, axiom, ? [P1, P2, P3, P4, P5, P6] :
    (six_way_tie_member(P1, du_maurier_1992) &
     six_way_tie_member(P2, du_maurier_1992) &
     six_way_tie_member(P3, du_maurier_1992) &
     six_way_tie_member(P4, du_maurier_1992) &
     six_way_tie_member(P5, du_maurier_1992) &
     six_way_tie_member(P6, du_maurier_1992) &
     P1 != P2 & P1 != P3 & P1 != P4 & P1 != P5 & P1 != P6 &
     P2 != P3 & P2 != P4 & P2 != P5 & P2 != P6 &
     P3 != P4 & P3 != P5 & P3 != P6 &
     P4 != P5 & P4 != P6 &
     P5 != P6)).
fof(conclusion, conjecture, six_way_tie_member(descampe, du_maurier_1992)).