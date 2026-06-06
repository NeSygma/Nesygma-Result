fof(p1, axiom, ! [X] : (from_istanbul(X) => begins_with_34(X))).
fof(p2, axiom, ! [X] : (~begins_with_34(X) => ~from_istanbul(X))).
fof(p3, axiom, from_istanbul(joe_plate)).
fof(p4, axiom, begins_with_35(tom_plate)).
fof(p5, axiom, ! [X] : (begins_with_35(X) => ~begins_with_34(X))).
fof(conclusion, conjecture, ~from_istanbul(tom_plate)).