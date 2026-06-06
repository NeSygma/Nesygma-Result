fof(premise1, axiom, ! [S] : (works_in_library(S) => ~cs_department(S))).
fof(premise2, axiom, ! [S] : (has_part_time_job(S) => works_in_library(S))).
fof(premise3, axiom, ! [S] : (taking_database_course(S) => cs_department(S))).
fof(premise4, axiom, ! [S] : (taking_class_with_professor_david(S) => taking_database_course(S))).
fof(premise5, axiom, ! [S] : (working_in_lab(S) => taking_class_with_professor_david(S))).
fof(premise6, axiom, working_in_lab(james)).
fof(premise7, axiom, ~has_part_time_job(james)).
fof(conclusion, conjecture, taking_database_course(james) | has_part_time_job(james)).