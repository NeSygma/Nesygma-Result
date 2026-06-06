% Negative version: negated conclusion as conjecture
% Negated conclusion: No design by Max is both evocative and dreamy.
% Formalized as: ~? [X] : (design_by_max(X) & evocative(X) & dreamy(X))
% Equivalent to: ! [X] : ~(design_by_max(X) & evocative(X) & dreamy(X))

fof(premise1, axiom, ! [X] : ((zaha_style(X) & adores(max, X)) => interesting_geometries(X))).

fof(premise2, axiom, ! [X] : ((brutalist(X) & adores(max, X)) => ~interesting_geometries(X))).

fof(premise3, axiom, ! [X] : (adores(max, X) => (zaha_style(X) | kelly_style(X)))).

fof(premise4, axiom, ! [X] : ((kelly_style(X) & adores(max, X)) => evocative(X))).

fof(premise5, axiom, ! [X] : ((kelly_style(X) & adores(max, X)) => dreamy(X))).

fof(premise6, axiom, ! [X] : ((design_by_max(X) & adores(max, X) & interesting_geometries(X)) => (brutalist(X) & evocative(X)))).

% Negated conclusion: No design by Max is both evocative and dreamy.
fof(negated_conclusion, conjecture, ! [X] : ~(design_by_max(X) & evocative(X) & dreamy(X))).