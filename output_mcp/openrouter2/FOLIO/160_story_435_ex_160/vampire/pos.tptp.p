fof(distinct, axiom, (james != david & james != cs & david != cs)).
fof(student_james, axiom, student(james)).
fof(works_in_lab_james, axiom, works_in_lab(james)).
fof(neg_lab_or_job, axiom, (~works_in_lab(james) | ~part_time_job_offered_by_university(james))).
fof(rule1, axiom, ! [X] : ((student(X) & works_in_library(X)) => ~from_department(X, cs))).
fof(rule2, axiom, ! [X] : ((student(X) & part_time_job_offered_by_university(X)) => works_in_library(X))).
fof(rule3, axiom, ! [X] : ((student(X) & takes_database_course(X)) => from_department(X, cs))).
fof(rule4, axiom, ! [X] : ((student(X) & takes_class_with_professor(X, david)) => takes_database_course(X))).
fof(rule5, axiom, ! [X] : ((student(X) & works_in_lab(X)) => takes_class_with_professor(X, david))).
fof(goal, conjecture, takes_database_course(james)).