fof(premise1, axiom, ? [X] : (professional_basketball_player(X) & ~american_national(X))).
fof(premise2, axiom, ! [X] : (professional_basketball_player(X) => can_jump_shot(X))).
fof(premise3, axiom, ! [X] : (can_jump_shot(X) => leaps_into_air(X))).
fof(premise4, axiom, ! [X] : (leaps_into_air(X) => activates_leg_muscles(X))).
fof(premise5, axiom, ~activates_leg_muscles(yuri)).

fof(conclusion, conjecture, (~american_national(yuri) & professional_basketball_player(yuri)) => professional_basketball_player(yuri)).