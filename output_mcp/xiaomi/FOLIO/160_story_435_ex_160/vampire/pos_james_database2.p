fof(p1, axiom, ! [X] : (works_in_library(X) => ~cs_dept(X))).
fof(p2, axiom, ! [X] : (part_time_uni(X) => works_in_library(X))).
fof(p3, axiom, ! [X] : (takes_database(X) => cs_dept(X))).
fof(p4, axiom, ! [X] : (takes_class_david(X) => takes_database(X))).
fof(p5, axiom, ! [X] : (works_in_lab(X) => takes_class_david(X))).
fof(p6, axiom, student(james) & works_in_lab(james)).
fof(p7, axiom, ~works_in_lab(james) | ~part_time_uni(james)).
fof(goal, conjecture, takes_database(james)).