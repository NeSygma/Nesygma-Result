fof(premise1, axiom, ? [X] : (basketball_player(X) & ~American(X))).
fof(premise2, axiom, ! [X] : (basketball_player(X) => can_jump_shot(X))).
fof(premise3, axiom, ! [X] : (can_jump_shot(X) => leap_straight_into_air(X))).
fof(premise4, axiom, ! [X] : (leap_straight_into_air(X) => activate_leg_muscles(X))).
fof(premise5, axiom, ~activate_leg_muscles(yuri)).
fof(neg_goal, conjecture, ~leap_straight_into_air(yuri) & ~(basketball_player(yuri) & American(yuri))).