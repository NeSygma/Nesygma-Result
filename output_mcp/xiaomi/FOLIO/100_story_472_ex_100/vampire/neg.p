% Premise 1: Animals are either invertebrates or vertebrates.
fof(p1, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).

% Premise 2: All animals with backbones reproduce by male-and-female mating.
fof(p2, axiom, ! [X] : ((animal(X) & backbone(X)) => reproduce_mf(X))).

% Premise 3: All vertebrate animals have a backbone.
fof(p3, axiom, ! [X] : ((animal(X) & vertebrate(X)) => backbone(X))).

% Premise 4: All bees do not reproduce by male-and-female mating.
fof(p4, axiom, ! [X] : (bee(X) => ~reproduce_mf(X))).

% Premise 5: All queen bees are bees.
fof(p5, axiom, ! [X] : (queen_bee(X) => bee(X))).

% Premise 6: Harry is a bee.
fof(p6, axiom, bee(harry)).

% Implicit: bees are animals
fof(p7, axiom, ! [X] : (bee(X) => animal(X))).

% Negated conclusion: ~(invertebrate(harry) | queen_bee(harry))
fof(goal, conjecture, ~(invertebrate(harry) | queen_bee(harry))).