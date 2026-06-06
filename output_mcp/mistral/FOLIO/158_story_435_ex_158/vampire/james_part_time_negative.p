fof(library_worker_not_cs, axiom, ! [S] : (works_in_library(S) => ~from_cs(S))).
fof(part_time_implies_library, axiom, ! [S] : (has_part_time_job(S) => works_in_library(S))).
fof(database_implies_cs, axiom, ! [S] : (taking_database(S) => from_cs(S))).
fof(prof_david_implies_database, axiom, ! [S] : (taking_prof_david(S) => taking_database(S))).
fof(works_lab_implies_prof_david, axiom, ! [S] : (works_in_lab(S) => taking_prof_david(S))).
fof(james_works_lab, axiom, works_in_lab(james)).
fof(james_no_lab_and_no_part_time, axiom, (~works_in_lab(james) & ~has_part_time_job(james))).
fof(goal_negation, conjecture, has_part_time_job(james)).