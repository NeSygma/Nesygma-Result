fof(some_not_american, axiom, ? [X] : (is_pro_basketball_player(X) & ~is_american_national(X))).
fof(all_can_jump_shots, axiom, ! [X] : (is_pro_basketball_player(X) => can_do_jump_shots(X))).
fof(jump_shots_to_leap, axiom, ! [X] : (can_do_jump_shots(X) => leaps_straight_into_air(X))).
fof(leap_to_activate, axiom, ! [X] : (leaps_straight_into_air(X) => activates_leg_muscles(X))).
fof(yuri_does_not_activate, axiom, ~activates_leg_muscles(yuri)).
fof(distinct_yuri, axiom, is_pro_basketball_player(yuri)).
fof(goal, conjecture, is_american_national(yuri)).