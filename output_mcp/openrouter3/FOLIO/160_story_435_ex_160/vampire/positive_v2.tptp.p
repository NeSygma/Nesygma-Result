% Positive version: James takes the database course
% Interpreting premise 7 as: James doesn't work in the LIBRARY or have a part-time job
fof(student_def, axiom, ! [X] : student(X)).  % All mentioned are students
fof(premise_1, axiom, ! [X] : (works_in_library(X) => ~from_cs_dept(X))).
fof(premise_2, axiom, ! [X] : (has_part_time_job(X) => works_in_library(X))).
fof(premise_3, axiom, ! [X] : (taking_database_course(X) => from_cs_dept(X))).
fof(premise_4, axiom, ! [X] : (taking_david_class(X) => taking_database_course(X))).
fof(premise_5, axiom, ! [X] : (works_in_lab(X) => taking_david_class(X))).
fof(premise_6, axiom, works_in_lab(james)).
fof(premise_7, axiom, ~works_in_library(james) & ~has_part_time_job(james)).
fof(goal, conjecture, taking_database_course(james)).