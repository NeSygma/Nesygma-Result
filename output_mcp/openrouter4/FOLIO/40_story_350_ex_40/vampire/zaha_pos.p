% Positive file: original claim as conjecture
% Premise 1
fof(premise1, axiom, ! [X] : ((zaha_style(X) & max_adores(X)) => interesting_geometries(X))).
% Premise 2
fof(premise2, axiom, ! [X] : ((brutalist(X) & max_adores(X)) => ~interesting_geometries(X))).
% Premise 3
fof(premise3, axiom, ! [X] : (max_adores(X) => (zaha_style(X) | kelly_style(X)))).
% Premise 4
fof(premise4, axiom, ! [X] : ((kelly_style(X) & max_adores(X)) => evocative(X))).
% Premise 5
fof(premise5, axiom, ! [X] : ((kelly_style(X) & max_adores(X)) => dreamy(X))).
% Premise 6
fof(premise6, axiom, ! [X] : ((by_max(X) & max_adores(X) & interesting_geometries(X)) => (brutalist(X) & evocative(X)))).
% Conclusion: A design by Max is a brutalist building (existential)
fof(goal, conjecture, ? [X] : (by_max(X) & brutalist(X))).