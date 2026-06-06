fof(ax1, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(ax2, axiom, ! [X] : ((animal(X) & has_backbone(X)) => reproduces_by_mating(X))).
fof(ax3, axiom, ! [X] : (vertebrate(X) => has_backbone(X))).
fof(ax4, axiom, ! [X] : (bee(X) => ~reproduces_by_mating(X))).
fof(ax5, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(fact_harry_bee, axiom, bee(harry)).
fof(goal, conjecture, ((vertebrate(harry) <=> has_backbone(harry)) => ((~invertebrate(harry)) & (~queen_bee(harry))))).