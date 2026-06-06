fof(hawk_no_swim, axiom, ! [X] : (hawk(X) => ~swims(X))).
fof(some_bird_is_hawk, axiom, ? [X] : (bird(X) & hawk(X))).
fof(conclusion, conjecture, ! [X] : (bird(X) => swims(X))).