fof(ax1, axiom, ! [X] : (alien(X) => extraterrestrial(X))).
fof(ax2, axiom, ! [X] : (from(X, mars) => alien(X))).
fof(ax3, axiom, ! [X] : (extraterrestrial(X) => ~human(X))).
fof(ax4, axiom, ! [X] : ((highly_intelligent(X) & from(X, earth)) => human(X))).
fof(fact_hi, axiom, highly_intelligent(marvin)).
fof(origin_disj, axiom, (from(marvin, earth) & from(marvin, mars)) | (~from(marvin, earth) & ~from(marvin, mars))).
fof(imp_not_earth, axiom, ~from(marvin, earth) => extraterrestrial(marvin)).
fof(goal, conjecture, ~alien(marvin)).