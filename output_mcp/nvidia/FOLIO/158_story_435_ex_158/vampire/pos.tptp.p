% FOF encoding of premises and conjecture ~has_part_time_job(james)
fof(none_cs_lib, axiom, ! [X] : (~works_in_lib(X) | ~from_cs_department(X))).
fof(all_part_time_lib, axiom, ! [X] : (~has_part_time_job(X) | works_in_lib(X))).
fof(all_db_cs, axiom, ! [X] : (~taking_database_course(X) | from_cs_department(X))).
fof(all_david_db, axiom, ! [X] : (~taking_class_with_david(X) | taking_database_course(X))).
fof(all_lab_david, axiom, ! [X] : (~works_in_lab(X) | taking_class_with_david(X))).
fof(james_works_lab, axiom, works_in_lab(james)).
fof(james_no_lab_or_part_job, axiom, (~works_in_lab(james) | ~has_part_time_job(james))).
fof(conclusion, conjecture, ~has_part_time_job(james)).