fof(exist_some, axiom, ? [X] : (professional_basketball_player(X) & ~american(X))).
fof(all_prof_can_jump, axiom, ! [X] : (professional_basketball_player(X) => can_jump_shot(X))).
fof(can_jump_implies_leap, axiom, ! [X] : (can_jump_shot(X) => leaps_straight_into_air(X))).
fof(leap_implies_activate, axiom, ! [X] : (leaps_straight_into_air(X) => activates_leg_muscles(X))).
fof(yuri_no_leg, axiom, ~activates_leg_muscles(yuri)).
fof(conjecture, conjecture, american(yuri) & professional_basketball_player(yuri)).