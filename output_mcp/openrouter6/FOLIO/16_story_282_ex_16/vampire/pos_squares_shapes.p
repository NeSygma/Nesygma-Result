fof(all_squares_four_sided, axiom, ! [X] : (square(X) => four_sided(X))).
fof(all_four_sided_shapes, axiom, ! [X] : (four_sided(X) => shape(X))).
fof(goal, conjecture, ! [X] : (square(X) => shape(X))).