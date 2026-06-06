fof(premise1, axiom, ? [X] : (pro_basketball_player(X) & ~american_national(X))).
fof(premise2, axiom, ! [X] : (pro_basketball_player(X) => can_jump_shot(X))).
fof(premise3, axiom, ! [X] : (can_jump_shot(X) => leaps_air(X))).
fof(premise4, axiom, ! [X] : (leaps_air(X) => activates_legs(X))).
fof(premise5, axiom, ~activates_legs(yuri)).
fof(conclusion, conjecture, (pro_basketball_player(yuri) & american_national(yuri))).