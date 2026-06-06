fof(premise1, axiom, ? [X] : (professional_basketball_player(X) & ~american(X))).
fof(premise2, axiom, ! [X] : (professional_basketball_player(X) => can_jump_shot(X))).
fof(premise3, axiom, ! [X] : (can_jump_shot(X) => leaps_straight(X))).
fof(premise4, axiom, ! [X] : (leaps_straight(X) => activates_leg_muscles(X))).
fof(premise5, axiom, ~activates_leg_muscles(yuri)).
fof(goal, conjecture, (~leaps_straight(yuri) => (american(yuri) & professional_basketball_player(yuri)))).