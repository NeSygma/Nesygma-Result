% Positive version: Original conclusion as conjecture
fof(premise_1, axiom, ! [X] : ((design(X) & max_adores(X) & zaha_hadid_style(X)) => interesting_geometries(X))).
fof(premise_2, axiom, ! [X] : ((design(X) & max_adores(X) & brutalist_building(X)) => ~interesting_geometries(X))).
fof(premise_3, axiom, ! [X] : ((design(X) & max_adores(X)) => (zaha_hadid_style(X) | kelly_wearstler_style(X)))).
fof(premise_4, axiom, ! [X] : ((design(X) & max_adores(X) & kelly_wearstler_style(X)) => evocative(X))).
fof(premise_5, axiom, ! [X] : ((design(X) & max_adores(X) & kelly_wearstler_style(X)) => dreamy(X))).
fof(premise_6, axiom, ! [X] : ((design(X) & max_adores(X) & interesting_geometries(X)) => (brutalist_building(X) & evocative(X)))).
fof(conclusion, conjecture, ! [X] : ((design(X) & max_adores(X)) => (evocative(X) | dreamy(X)))).