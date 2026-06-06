% Positive version
fof(ax1, axiom, ![X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(ax2, axiom, ![X] : (backbone(X) => reproduce_mf(X))).
fof(ax3, axiom, ![X] : ((animal(X) & vertebrate(X)) => backbone(X))).
fof(ax4, axiom, ![X] : (bee(X) => ~reproduce_mf(X))).
fof(ax5, axiom, ![X] : (queen_bee(X) => bee(X))).
fof(fact1, axiom, bee(harry)).
fof(goal_pos, conjecture, (invertebrate(harry) | queen_bee(harry))).