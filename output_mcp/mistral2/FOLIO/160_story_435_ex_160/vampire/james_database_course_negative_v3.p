fof(works_in_library_not_cs, axiom, ! [X] : (works_in_library(X) => ~computer_science(X))).
fof(part_time_job_implies_library, axiom, ! [X] : (has_part_time_job(X) => works_in_library(X))).
fof(database_course_implies_cs, axiom, ! [X] : (taking_database_course(X) => computer_science(X))).
fof(prof_david_implies_database, axiom, ! [X] : (taking_class_with_professor(X, david) => taking_database_course(X))).
fof(works_in_lab_implies_prof_david, axiom, ! [X] : (works_in_lab(X) => taking_class_with_professor(X, david))).
fof(james_works_in_lab, axiom, works_in_lab(james)).
fof(james_no_part_time, axiom, ~has_part_time_job(james)).
fof(distinct_constants, axiom, james != david).
fof(conclusion_negation, conjecture, ~taking_database_course(james)).