fof(premise1, axiom, ! [X] : (work_in_library(X) => ~from_cs(X))).
fof(premise2, axiom, ! [X] : (has_part_time_job(X) => work_in_library(X))).
fof(premise3, axiom, ! [X] : (takes_database(X) => from_cs(X))).
fof(premise4, axiom, ! [X] : (takes_class_with_david(X) => takes_database(X))).
fof(premise5, axiom, ! [X] : (work_in_lab(X) => takes_class_with_david(X))).
fof(premise6, axiom, work_in_lab(james)).
fof(premise7, axiom, ~work_in_library(james) & ~has_part_time_job(james)).
fof(neg_conclusion, conjecture, ~(takes_database(james) | has_part_time_job(james))).