% Negative version: Negated conclusion as conjecture
fof(premise_1, axiom, ? [X] : (professional_basketball_player(X) & ~american_national(X))).
fof(premise_2, axiom, ! [X] : (professional_basketball_player(X) => can_jump_shots(X))).
fof(premise_3, axiom, ! [X] : (can_jump_shots(X) => leaps_straight_into_air(X))).
fof(premise_4, axiom, ! [X] : (leaps_straight_into_air(X) => activates_leg_muscles(X))).
fof(premise_5, axiom, ~activates_leg_muscles(yuri)).
fof(goal_neg, conjecture, (~leaps_straight_into_air(yuri) & ~(professional_basketball_player(yuri) & american_national(yuri)))).