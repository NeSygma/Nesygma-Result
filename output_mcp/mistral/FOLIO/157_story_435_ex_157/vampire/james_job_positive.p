fof(premise1, axiom, ! [S] : (~works_in_library(S) | ~from_cs(S))).
fof(premise2, axiom, ! [S] : (~has_part_time_job(S) | works_in_library(S))).
fof(premise3, axiom, ! [S] : (~taking_database(S) | from_cs(S))).
fof(premise4, axiom, ! [S] : (~taking_prof_david(S) | taking_database(S))).
fof(premise5, axiom, ! [S] : (~works_in_lab(S) | taking_prof_david(S))).
fof(premise6, axiom, works_in_lab(james)).
fof(premise7, axiom, ~works_in_lab(james) | ~has_part_time_job(james)).
fof(conclusion, conjecture, has_part_time_job(james)).