fof(p1, axiom, ! [P] : (from_istanbul(P) => starts_with_34(P))).
fof(p2, axiom, ! [P] : (~starts_with_34(P) => ~from_istanbul(P))).
fof(p3, axiom, from_istanbul(joe_plate)).
fof(p4, axiom, starts_with_35(tom_plate)).
fof(p5, axiom, ! [P] : (starts_with_35(P) => ~starts_with_34(P))).
fof(goal, conjecture, ~starts_with_34(joe_plate)).