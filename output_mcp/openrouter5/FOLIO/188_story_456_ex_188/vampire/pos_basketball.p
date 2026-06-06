% Positive version: original conclusion as conjecture
% Premises:
% 1. Some professional basketball players are not American nationals.
fof(premise1, axiom, ? [X] : (professional_basketball_player(X) & ~american_national(X))).

% 2. All professional basketball players can do jump shots.
fof(premise2, axiom, ! [X] : (professional_basketball_player(X) => can_do_jump_shots(X))).

% 3. If someone can jump shots, they leap straight into the air.
fof(premise3, axiom, ! [X] : (can_do_jump_shots(X) => leaps_straight_into_air(X))).

% 4. If someone leaps straight into the air, they activate their leg muscles.
fof(premise4, axiom, ! [X] : (leaps_straight_into_air(X) => activates_leg_muscles(X))).

% 5. Yuri does not activate his leg muscles.
fof(premise5, axiom, ~activates_leg_muscles(yuri)).

% Conclusion: Yuri is an American national.
fof(conclusion, conjecture, american_national(yuri)).