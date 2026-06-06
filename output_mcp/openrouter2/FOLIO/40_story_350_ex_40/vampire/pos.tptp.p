fof(axiom1, axiom, ! [X] : ((zaha_style(X) & max_adore(X)) => interesting(X))).
fof(axiom2, axiom, ! [X] : ((brutalist(X) & max_adore(X)) => ~interesting(X))).
fof(axiom3, axiom, ! [X] : (max_adore(X) => (zaha_style(X) | kelly_style(X)))).
fof(axiom4, axiom, ! [X] : ((kelly_style(X) & max_adore(X)) => evocative(X))).
fof(axiom5, axiom, ! [X] : ((kelly_style(X) & max_adore(X)) => dreamy(X))).
fof(axiom6, axiom, ! [X] : ((design_by_max(X) & max_adore(X) & interesting(X)) => (brutalist(X) & evocative(X)))).
fof(conjecture, conjecture, ? [X] : (design_by_max(X) & brutalist(X))).