fof(prof_basketball_player_not_american, axiom, ? [X] : (professional_basketball_player(X) & ~american_national(X))).
fof(all_prof_can_jump, axiom, ! [X] : (professional_basketball_player(X) => jump_shot(X))).
fof(jump_shot_implies_leap, axiom, ! [X] : (jump_shot(X) => leap_straight_into_air(X))).
fof(leap_implies_activate, axiom, ! [X] : (leap_straight_into_air(X) => activate_leg_muscles(X))).
fof(yuri_not_activate, axiom, ~activate_leg_muscles(yuri)).
fof(conjecture, conjecture, american_national(yuri)).