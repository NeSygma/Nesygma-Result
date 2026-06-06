fof(premise_1, axiom, ! [X] : (from_istanbul(X) => begins_with_34(X))).
fof(premise_2, axiom, ! [X] : (~begins_with_34(X) => ~from_istanbul(X))).
fof(fact_joe, axiom, from_istanbul(joe)).
fof(fact_tom, axiom, begins_with_35(tom)).
fof(implication_35_34, axiom, ! [X] : (begins_with_35(X) => ~begins_with_34(X))).
fof(goal, conjecture, ~begins_with_34(joe)).