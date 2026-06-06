fof(istanbul_begin_34, axiom, ! [X] : (from_istanbul(X) => begins_with_34(X))).
fof(not_34_not_istanbul, axiom, ! [X] : (~begins_with_34(X) => ~from_istanbul(X))).
fof(joe_istanbul, axiom, from_istanbul(joe)).
fof(tom_begin_35, axiom, begins_with_35(tom)).
fof(begin_35_not_34, axiom, ! [X] : (begins_with_35(X) => ~begins_with_34(X))).
fof(goal, conjecture, from_istanbul(tom)).