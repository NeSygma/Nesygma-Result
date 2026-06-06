fof(premise_1, axiom, ! [P] : (from_istanbul(P) => begins_34(P))).
fof(premise_2, axiom, ! [P] : (~begins_34(P) => ~from_istanbul(P))).
fof(premise_3, axiom, from_istanbul(joe_plate)).
fof(premise_4, axiom, begins_35(tom_plate)).
fof(premise_5, axiom, ! [P] : (begins_35(P) => ~begins_34(P))).
fof(distinct, axiom, joe_plate != tom_plate).
fof(conclusion, conjecture, begins_34(joe_plate)).