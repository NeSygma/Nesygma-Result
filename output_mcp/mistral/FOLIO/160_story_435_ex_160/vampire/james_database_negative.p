fof(works_in_library_def, axiom, ! [S] : (works_in_library(S) => ~from_department(S, computer_science))).
fof(part_time_job_implies_library, axiom, ! [S] : (has_part_time_job(S) => works_in_library(S))).
fof(database_implies_cs_dept, axiom, ! [S] : (taking_database_course(S) => from_department(S, computer_science))).
fof(professor_david_implies_database, axiom, ! [S] : (taking_class_with_professor(S, professor_david) => taking_database_course(S))).
fof(works_in_lab_implies_professor_david, axiom, ! [S] : (works_in_lab(S) => taking_class_with_professor(S, professor_david))).
fof(james_works_in_lab, axiom, works_in_lab(james)).
fof(james_no_part_time_job, axiom, ~has_part_time_job(james)).
fof(conclusion_negation, conjecture, ~taking_database_course(james)).