fof(squares_are_four_sided, axiom, ! [X] : (square(X) => four_sided(X))).
fof(four_sided_are_shapes, axiom, ! [X] : (four_sided(X) => shape(X))).
fof(not_all_squares_are_shapes, conjecture, ~(! [X] : (square(X) => shape(X)))).