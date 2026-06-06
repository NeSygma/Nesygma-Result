% Negative version (negated conjecture)
fof(ax1, axiom, ! [X] : (hydrocarbon(X) => organic_compound(X))).
fof(ax2, axiom, ! [X] : (alkane(X) => hydrocarbon(X))).
fof(ax3, axiom, ! [X] : (organic_compound(X) => chemical_compound(X))).
fof(ax4, axiom, ! [X] : (organic_compound(X) => contains_carbon(X))).
fof(ax5, axiom, ! [X] : (chemical_compound(X) => ~contains_one_element(X))).
fof(ax6a, axiom, chemical_compound(mixture) => contains_one_element(mixture)).
fof(ax6b, axiom, contains_one_element(mixture) => chemical_compound(mixture)).
% Negated conjecture
fof(goal, conjecture, ~ (alkane(mixture) & contains_carbon(mixture))).