% Negative version (negated conjecture)
fof(ax1, axiom, ! [X] : (alien(X) => extraterrestrial(X))).
fof(ax2, axiom, ! [X] : (from_mars(X) => alien(X))).
fof(ax3, axiom, ! [X] : (extraterrestrial(X) => ~human(X))).
fof(ax4, axiom, ! [X] : ((highly_intelligent(X) & from_earth(X)) => human(X))).
fof(ax5, axiom, highly_intelligent(marvin)).
fof(ax6, axiom, ((from_earth(marvin) & from_mars(marvin)) | (~from_earth(marvin) & ~from_mars(marvin)))).
fof(ax7, axiom, (~from_earth(marvin) => extraterrestrial(marvin))).
fof(conj_neg, conjecture, (~from_mars(marvin) & ~human(marvin))).