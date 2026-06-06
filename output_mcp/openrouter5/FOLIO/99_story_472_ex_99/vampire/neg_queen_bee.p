% Negative file: negated claim as conjecture
% Premises:
% 1. Animals are either invertebrates or vertebrates.
fof(ax1, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
% 2. All animals with backbones reproduce by male-and-female mating.
fof(ax2, axiom, ! [X] : ((animal(X) & has_backbone(X)) => reproduces_mf(X))).
% 3. All vertebrate animals have a backbone.
fof(ax3, axiom, ! [X] : (vertebrate(X) => has_backbone(X))).
% 4. All bees do not reproduce by male-and-female mating.
fof(ax4, axiom, ! [X] : (bee(X) => ~reproduces_mf(X))).
% 5. All queen bees are bees.
fof(ax5, axiom, ! [X] : (queen_bee(X) => bee(X))).
% 6. Harry is a bee.
fof(ax6, axiom, bee(harry)).

% Negated conclusion: Harry is NOT a queen bee.
fof(goal_neg, conjecture, ~queen_bee(harry)).