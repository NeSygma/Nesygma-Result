fof(axiom_zaha_interesting, axiom, ! [S] : (zaha_style(S) & max_adores(S) => interesting_geometry(S))).
fof(axiom_no_brutalist_interesting, axiom, ! [S] : (brutalist(S) & max_adores(S) => ~interesting_geometry(S))).
fof(axiom_every_style_zaha_or_kelly, axiom, ! [S] : (max_adores(S) => (zaha_style(S) | kelly_style(S)))).
fof(axiom_kelly_evocative, axiom, ! [S] : (kelly_style(S) & max_adores(S) => evocative(S))).
fof(axiom_kelly_dreamy, axiom, ! [S] : (kelly_style(S) & max_adores(S) => dreamy(S))).
fof(axiom_design_implication, axiom, ! [D] : ((design_by_max(D) & max_adores(D) & interesting_geometry(D)) => (brutalist(D) & evocative(D)))).
fof(conclusion, conjecture, ! [X] : (design_by_max(X) => (evocative(X) | dreamy(X)))).