% Positive conjecture
fof(ax1, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(ax2, axiom, ! [X] : ((animal(X) & backbone(X)) => reproduce_mf(X))).
fof(ax3, axiom, ! [X] : (vertebrate(X) => backbone(X))).
fof(ax3a, axiom, ! [X] : (vertebrate(X) => animal(X))).
fof(ax4, axiom, ! [X] : (bee(X) => ~reproduce_mf(X))).
fof(ax5, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(fact1, axiom, bee(harry)).
fof(goal, conjecture, ((vertebrate(harry) & backbone(harry)) | (~vertebrate(harry) & ~backbone(harry))) => (~invertebrate(harry) & ~queen_bee(harry))).