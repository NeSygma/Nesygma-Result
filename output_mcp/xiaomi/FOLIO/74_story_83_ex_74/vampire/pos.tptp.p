fof(premise_1, axiom, ! [X] : (from_istanbul(X) => begins_with_34(X))).
fof(premise_2, axiom, ! [X] : (~begins_with_34(X) => ~from_istanbul(X))).
fof(premise_3, axiom, from_istanbul(joe)).
fof(premise_4, axiom, begins_with_35(tom)).
fof(premise_5, axiom, ! [X] : (begins_with_35(X) => ~begins_with_34(X))).
fof(conclusion, conjecture, begins_with_34(joe)).