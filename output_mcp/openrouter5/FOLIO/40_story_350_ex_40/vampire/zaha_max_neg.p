% Negative version: negated conclusion as conjecture
% "A design by Max is a brutalist building." - negated: ~(exists S: design_by_max(S) & brutalist(S))
% i.e., for all S, if design_by_max(S) then ~brutalist(S)

% Predicates:
% max_adore(S) - Max adores style S
% zaha_style(S) - S is a Zaha Hadid design style
% kelly_style(S) - S is a Kelly Wearstler design style
% interesting_geometries(S) - S has interesting geometries
% brutalist(S) - S is a brutalist building
% evocative(S) - S is evocative
% dreamy(S) - S is dreamy
% design_by_max(S) - S is a design by Max

% Premise 1: All of Zaha Hadid's design styles that Max adores have interesting geometries.
fof(p1, axiom, ! [S] : ((zaha_style(S) & max_adore(S)) => interesting_geometries(S))).

% Premise 2: No brutalist buildings that Max adores have interesting geometries.
fof(p2, axiom, ! [S] : ((brutalist(S) & max_adore(S)) => ~interesting_geometries(S))).

% Premise 3: Every style that Max adores is either Zaha Hadid's design style or Kelly Wearstler's design style.
fof(p3, axiom, ! [S] : (max_adore(S) => (zaha_style(S) | kelly_style(S)))).

% Premise 4: All of Kelly Wearstler's design styles that Max adores are evocative.
fof(p4, axiom, ! [S] : ((kelly_style(S) & max_adore(S)) => evocative(S))).

% Premise 5: All of Kelly Wearstler's design styles that Max adores are dreamy.
fof(p5, axiom, ! [S] : ((kelly_style(S) & max_adore(S)) => dreamy(S))).

% Premise 6: If a design by Max that he adores has interesting geometries, then the design is a brutalist building and evocative.
fof(p6, axiom, ! [S] : ((design_by_max(S) & max_adore(S) & interesting_geometries(S)) => (brutalist(S) & evocative(S)))).

% Negated conclusion: There is NO design by Max that is a brutalist building.
fof(goal_neg, conjecture, ! [S] : (design_by_max(S) => ~brutalist(S))).