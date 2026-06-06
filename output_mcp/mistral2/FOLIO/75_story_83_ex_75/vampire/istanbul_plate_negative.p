fof(plates_are_distinct, axiom, plate_joe != plate_tom).

fof(all_istanbul_plates_begin_with_34, axiom, ! [P] : (from_istanbul(P) => begins_with_34(P))).
fof(non_34_plates_not_from_istanbul, axiom, ! [P] : (~begins_with_34(P) => ~from_istanbul(P))).
fof(joe_plate_from_istanbul, axiom, from_istanbul(plate_joe)).
fof(tom_plate_begins_with_35, axiom, begins_with_35(plate_tom)).
fof(plate_begins_with_35_implies_not_34, axiom, ! [P] : (begins_with_35(P) => ~begins_with_34(P))).

fof(conclusion_negation, conjecture, ~from_istanbul(plate_tom)).