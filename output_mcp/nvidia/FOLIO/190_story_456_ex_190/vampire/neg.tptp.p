fof(prem2, axiom, ! [X] : (professional_basketball_player(X) => can_do_jump_shot(X))).
fof(prem3, axiom, ! [X] : (can_do_jump_shot(X) => leaps_straight_into_air(X))).
fof(prem4, axiom, ! [X] : (leaps_straight_into_air(X) => activates_leg_muscles(X))).
fof(prem5, axiom, ~activates_leg_muscles(yuri)).
fof(neg_goal, conjecture, ~american_national(yuri) | ~professional_basketball_player(yuri)).