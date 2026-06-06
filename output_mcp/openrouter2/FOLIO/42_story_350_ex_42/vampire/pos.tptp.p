fof(distinct_constants, axiom, (max != zaha_hadid & max != kelly_wearstler & zaha_hadid != kelly_wearstler)).
fof(design_adored_style, axiom, ! [X] : ((design_by_max(X) & adores(max, X)) => style(X))).
fof(style_adored_split, axiom, ! [X] : ((style(X) & adores(max, X)) => (zaha_hadid_style(X) | kelly_wearstler_style(X)))).
fof(zaha_interesting, axiom, ! [X] : ((zaha_hadid_style(X) & adores(max, X)) => interesting_geometry(X))).
fof(brutalist_no_interesting, axiom, ! [X] : ((brutalist(X) & adores(max, X)) => ~interesting_geometry(X))).
fof(kelly_evocative, axiom, ! [X] : ((kelly_wearstler_style(X) & adores(max, X)) => evocative(X))).
fof(kelly_dreamy, axiom, ! [X] : ((kelly_wearstler_style(X) & adores(max, X)) => dreamy(X))).
fof(design_interesting_implication, axiom, ! [X] : ((design_by_max(X) & adores(max, X) & interesting_geometry(X)) => (brutalist(X) & evocative(X)))).
fof(conjecture, conjecture, ! [X] : ((design_by_max(X)) => (evocative(X) | dreamy(X)))).