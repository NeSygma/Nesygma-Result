% Negative version
fof(ax1, axiom, ! [X] : (hydrocarbon(X) => organic(X))).
fof(ax2, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(ax3, axiom, ! [X] : (organic(X) => chemical(X))).
fof(ax4, axiom, ! [X] : (organic(X) => contains_carbon(X))).
fof(ax5, axiom, ! [X] : (chemical(X) => ~only_one(X))).
fof(ax6, axiom, (chemical(mixture) <=> only_one(mixture))).
fof(goal, conjecture, ~contains_carbon(mixture)).