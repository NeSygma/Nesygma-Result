% Negative version: negated conclusion as conjecture
% Harry is NOT (an invertebrate or a queen bee) i.e., Harry is not an invertebrate AND not a queen bee.

fof(distinct, axiom, (invertebrate != vertebrate)).
fof(rule1, axiom, ! [X] : (animal(X) => (invertebrate(X) | vertebrate(X)))).
fof(rule2, axiom, ! [X] : ((animal(X) & backbone(X)) => reproduce_mf(X))).
fof(rule3, axiom, ! [X] : (vertebrate(X) => backbone(X))).
fof(rule4, axiom, ! [X] : (bee(X) => ~reproduce_mf(X))).
fof(rule5, axiom, ! [X] : (queen_bee(X) => bee(X))).
fof(fact1, axiom, bee(harry)).
fof(goal, conjecture, (~invertebrate(harry) & ~queen_bee(harry))).