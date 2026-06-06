% Negative version (negated conclusion)
fof(ax1, axiom, ! [X] : ((zaha_hadid_style(X) & design_by_max(X) & adored(X)) => interesting_geometries(X))).
fof(ax2, axiom, ! [X] : ((brutalist(X) & design_by_max(X) & adored(X)) => ~interesting_geometries(X))).
fof(ax3, axiom, ! [X] : ((design_by_max(X) & adored(X)) => (zaha_hadid_style(X) | kelly_wearstler_style(X)))).
fof(ax4, axiom, ! [X] : ((kelly_wearstler_style(X) & design_by_max(X) & adored(X)) => evocative(X))).
fof(ax5, axiom, ! [X] : ((kelly_wearstler_style(X) & design_by_max(X) & adored(X)) => dreamy(X))).
fof(ax6, axiom, ! [X] : ((design_by_max(X) & adored(X) & interesting_geometries(X)) => (brutalist(X) & evocative(X)))).
fof(conj_neg, conjecture, ! [X] : ~ (design_by_max(X) & brutalist(X))).