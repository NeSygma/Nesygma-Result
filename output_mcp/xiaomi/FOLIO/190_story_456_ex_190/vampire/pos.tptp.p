fof(premise_1, axiom, ? [X] : (professional_basketball_player(X) & ~american(X))).
fof(premise_2, axiom, ! [X] : (professional_basketball_player(X) => can_jump_shot(X))).
fof(premise_3, axiom, ! [X] : (can_jump_shot(X) => leaps_straight(X))).
fof(premise_4, axiom, ! [X] : (leaps_straight(X) => activates_leg_muscles(X))).
fof(premise_5, axiom, ~activates_leg_muscles(yuri)).
fof(goal, conjecture, professional_basketball_player(yuri) & american(yuri)).