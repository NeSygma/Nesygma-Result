% Negative version: negated conclusion as conjecture
% Conclusion: Harry is an invertebrate or a queen bee.
% Negated: Harry is NOT an invertebrate AND NOT a queen bee.

% Animals are either invertebrates or vertebrates.
fof(axiom1, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).

% All animals with backbones reproduce by male-and-female mating.
fof(axiom2, axiom, ! [X] : ((animal(X) & has_backbone(X)) => reproduces_male_female(X))).

% All vertebrate animals have a backbone.
fof(axiom3, axiom, ! [X] : (vertebrate(X) => has_backbone(X))).

% All bees do not reproduce by male-and-female mating.
fof(axiom4, axiom, ! [X] : (bee(X) => ~reproduces_male_female(X))).

% All queen bees are bees.
fof(axiom5, axiom, ! [X] : (queen_bee(X) => bee(X))).

% Harry is a bee.
fof(axiom6, axiom, bee(harry)).

% Distinctness
fof(distinct, axiom, (harry = harry)).

% Negated conclusion: Harry is NOT an invertebrate AND NOT a queen bee.
fof(goal_neg, conjecture, (~invertebrate(harry) & ~queen_bee(harry))).