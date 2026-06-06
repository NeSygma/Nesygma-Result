fof(p1, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(p2, axiom, ! [X] : ((animal(X) & backbone(X)) => reproduce_mf(X))).
fof(p3, axiom, ! [X] : ((animal(X) & vertebrate(X)) => backbone(X))).
fof(p4, axiom, ! [X] : (bee(X) => ~reproduce_mf(X))).
fof(p5, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(p6, axiom, bee(harry)).

% Conclusion: condition => consequent
% condition: (vertebrate & animal & backbone) OR (~vertebrate & ~(animal & backbone))
% consequent: ~invertebrate & ~queen_bee
fof(goal, conjecture,
    (((vertebrate(harry) & animal(harry) & backbone(harry))
      | (~vertebrate(harry) & ~(animal(harry) & backbone(harry))))
     => (~invertebrate(harry) & ~queen_bee(harry)))).