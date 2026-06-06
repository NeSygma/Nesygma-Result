fof(exist1, axiom, ? [X] : (professional_basketball_player(X) & ~american(X))).
fof(rule2, axiom, ! [X] : ((professional_basketball_player(X) => jump_shot(X)))).
fof(rule3, axiom, ! [X] : ((jump_shot(X) => leap(X)))).
fof(rule4, axiom, ! [X] : ((leap(X) => activate_leg_muscles(X)))).
fof(fact5, axiom, ~activate_leg_muscles(yuri)).
fof(conjecture, conjecture, (~leap(yuri) => (american(yuri) & professional_basketball_player(yuri)))).