fof(premise1, axiom, ! [X] : (works_in_library(X) => ~from_cs(X))).
fof(premise2, axiom, ! [X] : (has_part_time_job(X) => works_in_library(X))).
fof(premise3, axiom, ! [X] : (takes_database(X) => from_cs(X))).
fof(premise4, axiom, ! [X] : (takes_david(X) => takes_database(X))).
fof(premise5, axiom, ! [X] : (works_in_lab(X) => takes_david(X))).
fof(premise6, axiom, works_in_lab(james)).
fof(premise7, axiom, ~works_in_library(james) & ~has_part_time_job(james)).
fof(goal, conjecture, takes_database(james)).