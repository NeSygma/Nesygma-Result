fof(premise_1, axiom, ! [P] : (plate_from_istanbul(P) => plate_begins_with_34(P))).
fof(premise_2, axiom, ! [P] : (~plate_begins_with_34(P) => ~plate_from_istanbul(P))).
fof(premise_3, axiom, plate_from_istanbul(joe)).
fof(premise_4, axiom, plate_begins_with_35(tom)).
fof(premise_5, axiom, ! [P] : (plate_begins_with_35(P) => ~plate_begins_with_34(P))).
fof(conclusion, conjecture, plate_begins_with_34(joe)).