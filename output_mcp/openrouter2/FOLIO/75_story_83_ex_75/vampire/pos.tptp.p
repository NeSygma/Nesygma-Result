fof(all_from_istanbul_begins_34, axiom, ! [X] : (from_istanbul(X) => begins_with_34(X))).
fof(not_begins_34_not_from_istanbul, axiom, ! [X] : (~begins_with_34(X) => ~from_istanbul(X))).
fof(joe_from_istanbul, axiom, from_istanbul(joe)).
fof(tom_begins_35, axiom, begins_with_35(tom)).
fof(begins_35_not_begins_34, axiom, ! [X] : (begins_with_35(X) => ~begins_with_34(X))).
fof(distinct, axiom, joe != tom).
fof(conjecture, conjecture, from_istanbul(tom)).