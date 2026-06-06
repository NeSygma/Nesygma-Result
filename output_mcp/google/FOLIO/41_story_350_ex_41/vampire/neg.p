fof(p1, axiom, ! [S] : ((zaha_hadid(S) & adores(max, S)) => interesting_geometries(S))).
fof(p2, axiom, ! [S] : ((brutalist(S) & adores(max, S)) => ~interesting_geometries(S))).
fof(p3, axiom, ! [S] : (adores(max, S) => (zaha_hadid(S) | kelly_wearstler(S)))).
fof(p4, axiom, ! [S] : ((kelly_wearstler(S) & adores(max, S)) => evocative(S))).
fof(p5, axiom, ! [S] : ((kelly_wearstler(S) & adores(max, S)) => dreamy(S))).
fof(p6, axiom, ! [S] : ((adores(max, S) & interesting_geometries(S)) => (brutalist(S) & evocative(S)))).
fof(goal, conjecture, ~ ? [S] : (adores(max, S) & evocative(S) & dreamy(S))).