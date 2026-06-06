fof(p1, axiom, ! [X] : (from_istanbul(X) => begins_34(X))).
fof(p2, axiom, ! [X] : (~begins_34(X) => ~from_istanbul(X))).
fof(p3, axiom, from_istanbul(joe)).
fof(p4, axiom, begins_35(tom)).
fof(p5, axiom, ! [X] : (begins_35(X) => ~begins_34(X))).
fof(distinct, axiom, joe != tom).
fof(goal, conjecture, begins_34(joe)).