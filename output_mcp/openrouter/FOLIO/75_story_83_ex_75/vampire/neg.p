fof(premise1, axiom, ! [X] : (from_istanbul(X) => begins34(X))).
fof(premise2, axiom, ! [X] : (~begins34(X) => ~from_istanbul(X))).
fof(premise3, axiom, from_istanbul(joe)).
fof(premise4, axiom, begins35(tom)).
fof(premise5, axiom, ! [X] : (begins35(X) => ~begins34(X))).
fof(distinct, axiom, joe != tom).
fof(goal, conjecture, ~from_istanbul(tom)).