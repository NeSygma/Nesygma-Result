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

% Distinctness: Yuri is a distinct individual (no other constants to distinguish)
% No other constants, so no distinctness axioms needed.

% Conclusion to evaluate:
% If Yuri is not an American professional basketball player, then Yuri is a professional basketball player.
% Formalized: (~american_professional_basketball_player(yuri) => professional_basketball_player(yuri))
% Where "American professional basketball player" means professional_basketball_player(yuri) & american_national(yuri)
% So: ~(professional_basketball_player(yuri) & american_national(yuri)) => professional_basketball_player(yuri)

fof(conclusion, conjecture, 
    (~(professional_basketball_player(yuri) & american_national(yuri)) => professional_basketball_player(yuri))).