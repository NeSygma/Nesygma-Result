% Positive version: original conclusion as conjecture
% Conclusion: A design by Max is evocative and dreamy.
% Formalized as: ? [D] : (design_by_max(D) & adores(max, D) & evocative(D) & dreamy(D))

% Predicates:
% zaha_style(X) - X is a Zaha Hadid design style
% adores(max, X) - Max adores X
% interesting_geometries(X) - X has interesting geometries
% brutalist(X) - X is a brutalist building
% kelly_style(X) - X is a Kelly Wearstler design style
% evocative(X) - X is evocative
% dreamy(X) - X is dreamy
% design_by_max(X) - X is a design by Max

% Premise 1: All of Zaha Hadid's design styles that Max adores have interesting geometries.
fof(premise1, axiom, ! [X] : ((zaha_style(X) & adores(max, X)) => interesting_geometries(X))).

% Premise 2: No brutalist buildings that Max adores have interesting geometries.
fof(premise2, axiom, ! [X] : ((brutalist(X) & adores(max, X)) => ~interesting_geometries(X))).

% Premise 3: Every style that Max adores is either Zaha Hadid's design style or Kelly Wearstler's design style.
fof(premise3, axiom, ! [X] : (adores(max, X) => (zaha_style(X) | kelly_style(X)))).

% Premise 4: All of Kelly Wearstler's design styles that Max adores are evocative.
fof(premise4, axiom, ! [X] : ((kelly_style(X) & adores(max, X)) => evocative(X))).

% Premise 5: All of Kelly Wearstler's design styles that Max adores are dreamy.
fof(premise5, axiom, ! [X] : ((kelly_style(X) & adores(max, X)) => dreamy(X))).

% Premise 6: If a design by Max that he adores has interesting geometries, then the design is a brutalist building and evocative.
fof(premise6, axiom, ! [X] : ((design_by_max(X) & adores(max, X) & interesting_geometries(X)) => (brutalist(X) & evocative(X)))).

% Conclusion: A design by Max is evocative and dreamy.
fof(conclusion, conjecture, ? [X] : (design_by_max(X) & evocative(X) & dreamy(X))).