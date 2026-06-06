fof(axiom1, axiom, ! [P] : (from_istanbul(P) => begins_with(P, n34))).
fof(axiom2, axiom, ! [P] : (~begins_with(P, n34) => ~from_istanbul(P))).
fof(axiom3, axiom, from_istanbul(plate_joe)).
fof(axiom4, axiom, begins_with(plate_tom, n35)).
fof(axiom5, axiom, ! [P] : (begins_with(P, n35) => ~begins_with(P, n34))).
fof(distinct_numbers, axiom, n34 != n35).
fof(distinct_plates, axiom, plate_joe != plate_tom).
fof(goal, conjecture, from_istanbul(plate_tom)).