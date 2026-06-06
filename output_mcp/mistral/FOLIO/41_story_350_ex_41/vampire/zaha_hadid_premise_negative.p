fof(premise1, axiom, ! [X] : ((zaha_design(X) & adores(max, X)) => interesting_geometries(X))).
fof(premise2, axiom, ! [X] : ((brutalist(X) & adores(max, X)) => ~interesting_geometries(X))).
fof(premise3, axiom, ! [X] : (adores(max, X) => (zaha_design(X) | kelly_design(X)))).
fof(premise4, axiom, ! [X] : ((kelly_design(X) & adores(max, X)) => evocative(X))).
fof(premise5, axiom, ! [X] : ((kelly_design(X) & adores(max, X)) => dreamy(X))).
fof(premise6, axiom, ! [X] : ((adores(max, X) & interesting_geometries(X)) => (brutalist(X) & evocative(X)))).
fof(goal_negation, conjecture, ! [X] : (~evocative(X) | ~dreamy(X))).