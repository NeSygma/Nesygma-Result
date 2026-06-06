% Positive version: original conclusion as conjecture
% Conclusion: If Yuri does not leap straight into the air, then Yuri is an American professional basketball player.
% Formalized: ~leaps(yuri) => (american(yuri) & professional_basketball_player(yuri))

fof(premise_1, axiom, ? [X] : (professional_basketball_player(X) & ~american_national(X))).
fof(premise_2, axiom, ! [X] : (professional_basketball_player(X) => can_do_jump_shots(X))).
fof(premise_3, axiom, ! [X] : (can_do_jump_shots(X) => leaps_straight_into_air(X))).
fof(premise_4, axiom, ! [X] : (leaps_straight_into_air(X) => activates_leg_muscles(X))).
fof(premise_5, axiom, ~activates_leg_muscles(yuri)).

fof(distinct, axiom, ! [X] : (american_national(X) => american(X))).

fof(goal, conjecture, (~leaps_straight_into_air(yuri) => (american(yuri) & professional_basketball_player(yuri)))).