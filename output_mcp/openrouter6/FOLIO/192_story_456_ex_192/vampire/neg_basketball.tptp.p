fof(premise1, axiom, ? [X] : (professional_basketball_player(X) & ~american_national(X))).
fof(premise2, axiom, ! [X] : (professional_basketball_player(X) => can_jump_shots(X))).
fof(premise3, axiom, ! [X] : (can_jump_shots(X) => leap_straight_into_air(X))).
fof(premise4, axiom, ! [X] : (leap_straight_into_air(X) => activate_leg_muscles(X))).
fof(premise5, axiom, ~activate_leg_muscles(yuri)).
fof(conclusion, conjecture, (~(professional_basketball_player(yuri) & american_national(yuri))) & ~professional_basketball_player(yuri)).