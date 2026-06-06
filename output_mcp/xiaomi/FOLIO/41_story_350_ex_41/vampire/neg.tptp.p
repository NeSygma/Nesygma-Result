fof(p1, axiom, ! [X] : ((zaha_hadid_style(X) & max_adores(X)) => interesting_geometry(X))).
fof(p2, axiom, ! [X] : ((brutalist_building(X) & max_adores(X)) => ~interesting_geometry(X))).
fof(p3, axiom, ! [X] : (max_adores(X) => (zaha_hadid_style(X) | kelly_wearstler_style(X)))).
fof(p4, axiom, ! [X] : ((kelly_wearstler_style(X) & max_adores(X)) => evocative(X))).
fof(p5, axiom, ! [X] : ((kelly_wearstler_style(X) & max_adores(X)) => dreamy(X))).
fof(p6, axiom, ! [X] : ((design_by_max(X) & max_adores(X) & interesting_geometry(X)) => (brutalist_building(X) & evocative(X)))).
fof(existence, axiom, ? [X] : (design_by_max(X) & max_adores(X))).
fof(goal, conjecture, ~? [X] : (design_by_max(X) & evocative(X) & dreamy(X))).