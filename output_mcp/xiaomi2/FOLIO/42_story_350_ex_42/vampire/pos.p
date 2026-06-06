fof(p1, axiom, ! [X] : ((zaha_hadid_style(X) & adores(max, X)) => interesting_geometry(X))).
fof(p2, axiom, ! [X] : ((brutalist(X) & adores(max, X)) => ~interesting_geometry(X))).
fof(p3, axiom, ! [X] : (adores(max, X) => (zaha_hadid_style(X) | kelly_wearstler_style(X)))).
fof(p4, axiom, ! [X] : ((kelly_wearstler_style(X) & adores(max, X)) => evocative(X))).
fof(p5, axiom, ! [X] : ((kelly_wearstler_style(X) & adores(max, X)) => dreamy(X))).
fof(p6, axiom, ! [X] : ((design_by_max(X) & adores(max, X) & interesting_geometry(X)) => (brutalist(X) & evocative(X)))).
fof(goal, conjecture, ! [X] : ((design_by_max(X) & adores(max, X)) => (evocative(X) | dreamy(X)))).