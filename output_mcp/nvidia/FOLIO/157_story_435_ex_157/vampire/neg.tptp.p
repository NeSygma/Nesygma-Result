fof(premise1, axiom, ! [X] : ((student(X) & works_in_library(X)) => ~from_cs(X)).
fof(premise2, axiom, ! [X] : ((student(X) & pjob(X)) => works_in_library(X)).
fof(premise3, axiom, ! [X] : ((taking_db(X) & student(X)) => from_cs(X)).
fof(premise4, axiom, ! [X] : ((taking_class_with_david(X) & student(X)) => taking_db(X)).
fof(premise5, axiom, ! [X] : ((works_in_lab(X) & student(X)) => taking_class_with_david(X)).
fof(fact_student_james, axiom, student(james)).
fof(fact_works_in_lab_james, axiom, works_in_lab(james)).
fof(premise7, axiom, ~works_in_lab(james) | pjob(james)).
fof(neg_conjecture, conjecture, ~pjob(james)).