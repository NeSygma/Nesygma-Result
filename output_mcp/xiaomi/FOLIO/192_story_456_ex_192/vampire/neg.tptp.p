fof(premise1, axiom, ? [X] : (professional_basketball_player(X) & ~american_national(X))).
fof(premise2, axiom, ! [X] : (professional_basketball_player(X) => can_jump_shot(X))).
fof(premise3, axiom, ! [X] : (can_jump_shot(X) => leaps_straight_up(X))).
fof(premise4, axiom, ! [X] : (leaps_straight_up(X) => activates_leg_muscles(X))).
fof(premise5, axiom, ~activates_leg_muscles(yuri)).
fof(distinct, axiom, yuri != skolem_1).
fof(goal, conjecture, ~(~american_national(yuri) => professional_basketball_player(yuri))).