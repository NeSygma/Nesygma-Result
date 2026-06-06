fof(premise1, axiom, ! [X] : ((zaha_hadid_style(X) & max_adores(X)) => interesting_geometries(X))).
fof(premise2, axiom, ! [X] : ((brutalist_building(X) & max_adores(X)) => ~interesting_geometries(X))).
fof(premise3, axiom, ! [X] : (max_adores(X) => (zaha_hadid_style(X) | kelly_wearstler_style(X)))).
fof(premise4, axiom, ! [X] : ((kelly_wearstler_style(X) & max_adores(X)) => evocative(X))).
fof(premise5, axiom, ! [X] : ((kelly_wearstler_style(X) & max_adores(X)) => dreamy(X))).
fof(premise6, axiom, ! [X] : ((max_adores(X) & interesting_geometries(X)) => (brutalist_building(X) & evocative(X)))).
fof(goal, conjecture, ! [X] : (max_adores(X) => ~brutalist_building(X))).