% Negative conjecture (negation of existence)
fof(premise1, axiom, ! [X] : ( (zaha_hadid_style(X) & max_adores(X)) => interesting_geom(X) ) ).
fof(premise2, axiom, ! [X] : ( (brutalist(X) & max_adores(X)) => ~interesting_geom(X) ) ).
fof(premise3, axiom, ! [X] : ( max_adores(X) => (zaha_hadid_style(X) | kelly_wearstler_style(X)) ) ).
fof(premise4, axiom, ! [X] : ( (kelly_wearstler_style(X) & max_adores(X)) => evocative(X) ) ).
fof(premise5, axiom, ! [X] : ( (kelly_wearstler_style(X) & max_adores(X)) => dreamy(X) ) ).
fof(premise6, axiom, ! [X] : ( (max_adores(X) & interesting_geom(X)) => (brutalist(X) & evocative(X)) ) ).
fof(goal_neg, conjecture, ! [X] : ( max_adores(X) => ~(evocative(X) & dreamy(X)) ) ).