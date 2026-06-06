fof(winner, axiom, winner(steinhauer, dmc)).
fof(participated, axiom, participated(steinhauer, dmc)).
fof(six_way_tie_exists, axiom, ? [X1, X2, X3, X4, X5, X6] : (
    in_six_way_tie(X1) & in_six_way_tie(X2) & in_six_way_tie(X3) & 
    in_six_way_tie(X4) & in_six_way_tie(X5) & in_six_way_tie(X6) &
    X1 != X2 & X1 != X3 & X1 != X4 & X1 != X5 & X1 != X6 &
    X2 != X3 & X2 != X4 & X2 != X5 & X2 != X6 &
    X3 != X4 & X3 != X5 & X3 != X6 &
    X4 != X5 & X4 != X6 &
    X5 != X6 &
    ! [Y] : (in_six_way_tie(Y) => (Y=X1 | Y=X2 | Y=X3 | Y=X4 | Y=X5 | Y=X6))
)).
fof(tie_on_leaderboard, axiom, ! [X] : (in_six_way_tie(X) => on_leaderboard(X, dmc))).
fof(belgian_in_tie, axiom, ? [X] : (in_six_way_tie(X) & from_belgium(X))).
fof(descampe_info, axiom, from_belgium(descampe) & on_leaderboard(descampe, dmc)).
fof(leaderboard_participated, axiom, ! [X] : (on_leaderboard(X, dmc) => participated(X, dmc))).
fof(distinct_people, axiom, (steinhauer != descampe)).

fof(goal, conjecture, ~in_six_way_tie(descampe)).