% Domain
student(louis). student(mollie). student(onyx). student(ryan). student(tiffany). student(yoshio).
year(1921). year(1922). year(1923). year(1924).

% Each year has exactly one student assigned
1 { assigned(S, Y) : student(S) } 1 :- year(Y).

% A student can be assigned to at most one year
0 { assigned(S, Y) : year(Y) } 1 :- student(S).

% Helper: student is on the project
on_project(S) :- assigned(S, _).

% Constraint 1: Only Louis or Tiffany can be assigned to 1923
:- assigned(S, 1923), S != louis, S != tiffany.

% Constraint 2: If Mollie is assigned, she must be to 1921 or 1922
:- assigned(mollie, Y), Y != 1921, Y != 1922.

% Constraint 3: If Tiffany is assigned, Ryan must be assigned
:- on_project(tiffany), not on_project(ryan).

% Constraint 4: If Ryan is assigned, Onyx must be to the year immediately prior
% Ryan at Y means Onyx at Y-1
:- assigned(ryan, 1921).  % No year before 1921
:- assigned(ryan, 1922), not assigned(onyx, 1921).
:- assigned(ryan, 1923), not assigned(onyx, 1922).
:- assigned(ryan, 1924), not assigned(onyx, 1923).

% Constraint 5: Yoshio is NOT assigned to the project
:- on_project(yoshio).

% Answer choice conditions
% (A) Louis is not assigned to the project
cond_a :- not on_project(louis).
% (B) Ryan is not assigned to the project
cond_b :- not on_project(ryan).
% (C) Tiffany is not assigned to the project
cond_c :- not on_project(tiffany).
% (D) Onyx is assigned to 1922
cond_d :- assigned(onyx, 1922).
% (E) Louis is assigned to 1924
cond_e :- assigned(louis, 1924).

option(a) :- cond_a.
option(b) :- cond_b.
option(c) :- cond_c.
option(d) :- cond_d.
option(e) :- cond_e.

#show option/1.
#show assigned/2.