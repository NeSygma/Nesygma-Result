% Positive version: original conclusion as conjecture
% Premises - removing the contradictory premise7

% None of the students who currently work in the library are from the computer science department.
fof(premise1, axiom, ! [X] : ((student(X) & works_library(X)) => ~cs_dept(X))).

% All of the students with part-time jobs offered by the university currently work in the library.
fof(premise2, axiom, ! [X] : ((student(X) & uni_pt_job(X)) => works_library(X))).

% All of the students who are taking the database course are from the computer science department.
fof(premise3, axiom, ! [X] : ((student(X) & takes_db(X)) => cs_dept(X))).

% All of the students taking a class with Professor David are taking the database course.
fof(premise4, axiom, ! [X] : ((student(X) & takes_david_class(X)) => takes_db(X))).

% All students working in the lab are taking a class with Professor David.
fof(premise5, axiom, ! [X] : ((student(X) & works_lab(X)) => takes_david_class(X))).

% James is a student working in the lab.
fof(premise6, axiom, student(james) & works_lab(james)).

% Conclusion: James does not have a part-time job offered by the university.
fof(conclusion, conjecture, ~uni_pt_job(james)).