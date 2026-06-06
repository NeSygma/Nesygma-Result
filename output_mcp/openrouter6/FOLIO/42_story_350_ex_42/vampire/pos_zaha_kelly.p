fof(premise1, axiom, ! [X] : ((zaha_hadid_style(X) & adores_max(X)) => interesting_geometries(X))).
fof(premise2, axiom, ! [X] : ((brutalist_building(X) & adores_max(X)) => ~interesting_geometries(X))).
fof(premise3, axiom, ! [X] : (adores_max(X) => (zaha_hadid_style(X) | kelly_wearstler_style(X)))).
fof(premise4, axiom, ! [X] : ((kelly_wearstler_style(X) & adores_max(X)) => evocative(X))).
fof(premise5, axiom, ! [X] : ((kelly_wearstler_style(X) & adores_max(X)) => dreamy(X))).
fof(premise6, axiom, ! [X] : ((adores_max(X) & interesting_geometries(X)) => (brutalist_building(X) & evocative(X)))).
fof(conclusion, conjecture, ! [X] : (adores_max(X) => (evocative(X) | dreamy(X)))).