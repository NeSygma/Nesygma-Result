fof(prof_player_a1, axiom, professional_basketball_player(a1)).
fof(not_american_a1, axiom, ~american(a1)).
fof(distinct_a1_yuri, axiom, a1 != yuri).
fof(all_prof_can_jump, axiom, ! [X] : (professional_basketball_player(X) => jump_shot(X))).
fof(all_jump_leap, axiom, ! [X] : (jump_shot(X) => leap_straight_into_air(X))).
fof(all_leap_activate, axiom, ! [X] : (leap_straight_into_air(X) => activate_leg_muscles(X))).
fof(yuri_not_activate, axiom, ~activate_leg_muscles(yuri)).
fof(goal, conjecture, american(yuri) & professional_basketball_player(yuri)).