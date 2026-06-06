fof(axiom_1, axiom, ? [X] : (professional_basketball_player(X) & ~american_national(X))).
fof(axiom_2, axiom, ! [X] : (professional_basketball_player(X) => can_jump_shots(X))).
fof(axiom_3, axiom, ! [X] : (can_jump_shots(X) => leaps_straight_into_air(X))).
fof(axiom_4, axiom, ! [X] : (leaps_straight_into_air(X) => activates_leg_muscles(X))).
fof(axiom_5, axiom, ~activates_leg_muscles(yuri)).
fof(conclusion, conjecture, professional_basketball_player(yuri)).