fof(premise1, axiom, ? [X] : (professional_basketball_player(X) & ~american_national(X))).
fof(premise2, axiom, ! [X] : (professional_basketball_player(X) => can_do_jump_shot(X))).
fof(premise3, axiom, ! [X] : (can_do_jump_shot(X) => leap_straight_into_air(X))).
fof(premise4, axiom, ! [X] : (leap_straight_into_air(X) => activate_leg_muscles(X))).
fof(premise5, axiom, ~activate_leg_muscles(yuri)).
fof(neg_conclusion, conjecture, ((~(american_national(yuri) & professional_basketball_player(yuri))) & ~professional_basketball_player(yuri))).