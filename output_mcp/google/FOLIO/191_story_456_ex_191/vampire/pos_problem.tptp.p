fof(p1, axiom, ? [X] : (pro_basketball_player(X) & ~american(X))).
fof(p2, axiom, ! [X] : (pro_basketball_player(X) => can_jump_shot(X))).
fof(p3, axiom, ! [X] : (can_jump_shot(X) => leaps_straight(X))).
fof(p4, axiom, ! [X] : (leaps_straight(X) => activates_leg_muscles(X))).
fof(p5, axiom, ~activates_leg_muscles(yuri)).
fof(goal, conjecture, (~leaps_straight(yuri) => (american(yuri) & pro_basketball_player(yuri)))).