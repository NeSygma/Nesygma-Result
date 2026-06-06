fof(all_vehicles_from_istanbul, axiom, ! [X]: (from_istanbul(X) => begins_with_34(X))).
fof(no_plate_without_34_from_istanbul, axiom, ! [X]: (~begins_with_34(X) => ~from_istanbul(X))).
fof(joe_from_istanbul, axiom, from_istanbul(joe)).
fof(tom_begins_with_35, axiom, begins_with_35(tom)).
fof(begin_35_implies_not_34, axiom, begins_with_35(tom) => ~begins_with_34(tom)).
fof(goal, conjecture, from_istanbul(tom)).