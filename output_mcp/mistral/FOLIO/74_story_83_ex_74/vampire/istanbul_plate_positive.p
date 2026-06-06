fof(from_istanbul_implies_34, axiom, ! [P] : (from_istanbul(P) => begins_with_34(P))).
fof(joe_from_istanbul, axiom, from_istanbul(joe_plate)).
fof(tom_begins_with_35, axiom, begins_with_35(tom_plate)).
fof(plate_35_implies_not_34, axiom, ! [P] : (begins_with_35(P) => ~begins_with_34(P))).
fof(distinct_plates, axiom, joe_plate != tom_plate).
fof(goal, conjecture, begins_with_34(joe_plate)).