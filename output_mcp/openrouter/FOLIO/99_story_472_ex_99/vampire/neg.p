% Negative test (negated conjecture)
fof(ax1, axiom, ! [X] : (vertebrate(X) => backbone(X))).
fof(ax2, axiom, ! [X] : (backbone(X) => reproduce_by_mf_mating(X))).
fof(ax3, axiom, ! [X] : (bee(X) => ~reproduce_by_mf_mating(X))).
fof(ax4, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(ax5, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(fact1, axiom, bee(harry)).
fof(goal, conjecture, ~queen_bee(harry)).