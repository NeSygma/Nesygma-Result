fof(ax1, axiom, ! [X] : (brown_swiss(X) => cow(X))).
fof(ax2, axiom, ? [X] : (pet(X) & brown_swiss(X))).
fof(ax3, axiom, ! [X] : (cow(X) => domesticated(X))).
fof(ax4, axiom, ! [X] : (alligator(X) => ~domesticated(X))).
fof(ax5, axiom, alligator(ted)).
fof(goal, conjecture, brown_swiss(ted) => ~pet(ted)).