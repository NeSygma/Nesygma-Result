% Positive version: conjecture is "James has a part-time job offered by the university"
% Predicates:
%   student(X)          - X is a student
%   library_worker(X)   - X currently works in the library
%   cs_dept(X)          - X is from the computer science department
%   pt_job_uni(X)       - X has a part-time job offered by the university
%   db_course(X)        - X is taking the database course
%   class_with_david(X) - X is taking a class with Professor David
%   lab_worker(X)       - X works in the lab

fof(premise_1, axiom, ! [X] : ((student(X) & library_worker(X)) => ~cs_dept(X))).
fof(premise_2, axiom, ! [X] : ((student(X) & pt_job_uni(X)) => library_worker(X))).
fof(premise_3, axiom, ! [X] : ((student(X) & db_course(X)) => cs_dept(X))).
fof(premise_4, axiom, ! [X] : ((student(X) & class_with_david(X)) => db_course(X))).
fof(premise_5, axiom, ! [X] : ((student(X) & lab_worker(X)) => class_with_david(X))).
fof(premise_6, axiom, student(james)).
fof(premise_7, axiom, lab_worker(james)).
fof(premise_8, axiom, ~lab_worker(james) | ~pt_job_uni(james)).

fof(goal, conjecture, pt_job_uni(james)).