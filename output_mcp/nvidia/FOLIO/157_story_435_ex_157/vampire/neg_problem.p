fof(premise1, axiom, ! [X] : (works_in(X, library) => ~from_department(X, cs_dept))).
fof(premise2, axiom, ! [X] : (has_part_time_job(X) => works_in(X, library))).
fof(premise3, axiom, ! [X] : (takes_course(X, database_course) => from_department(X, cs_dept))).
fof(premise4, axiom, ! [X] : (takes_class(X, professor_david) => takes_course(X, database_course))).
fof(premise5, axiom, ! [X] : (works_in(X, lab) => takes_class(X, professor_david))).
fof(premise6, axiom, works_in(james, lab)).
fof(premise7, axiom, ~works_in(james, lab) | has_part_time_job(james)).
fof(conjecture, conjecture, ~has_part_time_job(james)).