fof(ax1, axiom, ! [X] : (brown_swiss_cattle(X) => cow(X))).
fof(ax2, axiom, ? [X] : (pet(X) & brown_swiss_cattle(X))).
fof(ax3, axiom, ! [X] : (cow(X) => domesticated(X))).
fof(ax4, axiom, ! [X] : (alligator(X) => ~domesticated(X))).
fof(ax5, axiom, alligator(ted)).
fof(goal, conjecture, ~ (pet(ted) & brown_swiss_cattle(ted))).