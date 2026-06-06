fof(premise_1, axiom, ! [X] : (library_work(X) => ~cs_dept(X))).
fof(premise_2, axiom, ! [X] : (part_time_job(X) => library_work(X))).
fof(premise_3, axiom, ! [X] : (database_course(X) => cs_dept(X))).
fof(premise_4, axiom, ! [X] : (david_class(X) => database_course(X))).
fof(premise_5, axiom, ! [X] : (lab_work(X) => david_class(X))).
fof(premise_6, axiom, lab_work(james)).
fof(premise_7, axiom, ~library_work(james) & ~part_time_job(james)).
fof(goal, conjecture, database_course(james)).