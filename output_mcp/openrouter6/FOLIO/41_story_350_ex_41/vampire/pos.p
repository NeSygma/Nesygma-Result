fof(premise1, axiom, ! [X] : ((adores(X) & zaha_hadid_style(X)) => interesting_geometries(X))).
fof(premise2, axiom, ! [X] : ((adores(X) & brutalist_building(X)) => ~interesting_geometries(X))).
fof(premise3, axiom, ! [X] : (adores(X) => (zaha_hadid_style(X) | kelly_wearstler_style(X)))).
fof(premise4, axiom, ! [X] : ((adores(X) & kelly_wearstler_style(X)) => evocative(X))).
fof(premise5, axiom, ! [X] : ((adores(X) & kelly_wearstler_style(X)) => dreamy(X))).
fof(premise6, axiom, ! [X] : ((adores(X) & interesting_geometries(X)) => (brutalist_building(X) & evocative(X)))).
fof(goal, conjecture, ? [X] : (adores(X) & evocative(X) & dreamy(X))).