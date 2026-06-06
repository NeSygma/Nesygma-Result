% Positive version: test if conclusion follows from premises
% Conclusion: James does not have a part-time job offered by the university

% Predicates:
% works_library(X) - X currently works in the library
% cs_dept(X) - X is from the computer science department
% pt_job_univ(X) - X has a part-time job offered by the university
% takes_database(X) - X is taking the database course
% takes_class_david(X) - X is taking a class with Professor David
% works_lab(X) - X is working in the lab

fof(premise_1, axiom, ! [X] : (works_library(X) => ~cs_dept(X))).
fof(premise_2, axiom, ! [X] : (pt_job_univ(X) => works_library(X))).
fof(premise_3, axiom, ! [X] : (takes_database(X) => cs_dept(X))).
fof(premise_4, axiom, ! [X] : (takes_class_david(X) => takes_database(X))).
fof(premise_5, axiom, ! [X] : (works_lab(X) => takes_class_david(X))).
fof(premise_6, axiom, works_lab(james)).
% Premise 7: "James doesn't work in the lab or have a part-time job offered by the university."
% Natural reading: James does not (work in the lab or have a part-time job) = ~works_lab(james) & ~pt_job_univ(james)
fof(premise_7, axiom, ~(works_lab(james) | pt_job_univ(james))).

% Conclusion to evaluate: James does not have a part-time job offered by the university.
fof(conclusion, conjecture, ~pt_job_univ(james)).