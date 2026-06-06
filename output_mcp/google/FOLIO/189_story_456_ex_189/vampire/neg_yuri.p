fof(p1, axiom, ? [X] : (pro_bb_player(X) & ~american(X))).
fof(p2, axiom, ! [X] : (pro_bb_player(X) => can_jump_shot(X))).
fof(p3, axiom, ! [X] : (can_jump_shot(X) => leap_air(X))).
fof(p4, axiom, ! [X] : (leap_air(X) => activate_leg_muscles(X))).
fof(p5, axiom, ~activate_leg_muscles(yuri)).
fof(goal, conjecture, (american(yuri) & pro_bb_player(yuri))).