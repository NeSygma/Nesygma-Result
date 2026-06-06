fof(premise1, axiom, ! [X] : (works_in_library(X) => ~from_cs(X))).
fof(premise2, axiom, ! [X] : (has_part_time_job(X) => works_in_library(X))).
fof(premise3, axiom, ! [X] : (takes_database(X) => from_cs(X))).
fof(premise4, axiom, ! [X] : (takes_david_class(X) => takes_database(X))).
fof(premise5, axiom, ! [X] : (works_in_lab(X) => takes_david_class(X))).
fof(premise6, axiom, works_in_lab(james)).
fof(premise7, axiom, ~works_in_lab(james) | ~has_part_time_job(james)).
fof(goal, conjecture, ~has_part_time_job(james)).