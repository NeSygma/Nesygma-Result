% Positive version
fof(premise1, axiom, ? [X] : (professional(X) & ~american(X))).
fof(premise2, axiom, ! [X] : (professional(X) => can_jump_shot(X))).
fof(premise3, axiom, ! [X] : (can_jump_shot(X) => leap_straight(X))).
fof(premise4, axiom, ! [X] : (leap_straight(X) => activate_leg_muscles(X))).
fof(premise5, axiom, ~activate_leg_muscles(yuri)).
fof(goal, conjecture, american(yuri) & professional(yuri)).