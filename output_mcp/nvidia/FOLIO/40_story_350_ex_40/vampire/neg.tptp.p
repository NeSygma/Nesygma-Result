% Axioms
fof(axiom1, axiom, ! [X] : (zaha_design(X) & max_adores(X) => interesting_geometry(X))).
fof(axiom2, axiom, ! [X] : (brutalist_building(X) & max_adores(X) => ~interesting_geometry(X))).
fof(axiom3, axiom, ! [X] : (max_adores(X) => (zaha_design(X) | kelly_design(X)))).
fof(axiom4, axiom, ! [X] : (kelly_design(X) & max_adores(X) => evocative(X))).
fof(axiom5, axiom, ! [X] : (kelly_design(X) & max_adores(X) => dreamy(X))).
fof(axiom6, axiom, ! [X] : (max_design(X) & max_adores(X) & interesting_geometry(X) => (brutalist_building(X) & evocative(X)))).
fof(neg_conjecture, conjecture, ~(max_design(X) & brutalist_building(X))).