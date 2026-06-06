fof(exist_some, axiom, ? [X] : (professional_basketball_player(X) & ~american_national(X))).
fof(rule1, axiom, ! [X] : (professional_basketball_player(X) => jump_shot(X))).
fof(rule2, axiom, ! [X] : (jump_shot(X) => leap_straight_into_air(X))).
fof(rule3, axiom, ! [X] : (leap_straight_into_air(X) => activate_leg_muscles(X))).
fof(yuri_no_activate, axiom, ~activate_leg_muscles(yuri)).
fof(conjecture, conjecture, ~((~(professional_basketball_player(yuri) & american_national(yuri))) => professional_basketball_player(yuri))).