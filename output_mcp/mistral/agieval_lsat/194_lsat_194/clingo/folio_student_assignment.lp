% Define years and students
year(1921). year(1922). year(1923). year(1924).
student(louis). student(mollie). student(onyx). student(ryan). student(tiffany). student(yoshio).

% Each year has exactly one student assigned
1 { assigned(S, Y) : student(S) } 1 :- year(Y).

% Constraint 1: Only Louis or Tiffany can be assigned to 1923
:- assigned(S, 1923), S != louis, S != tiffany.

% Constraint 2: If Mollie is assigned, she must be assigned to 1921 or 1922
:- assigned(mollie, Y), Y != 1921, Y != 1922.

% Constraint 3: If Tiffany is assigned, then Ryan must be assigned
:- assigned(tiffany, _), not assigned(ryan, _).

% Constraint 4: If Ryan is assigned, then Onyx must be assigned to the year immediately prior
:- assigned(ryan, 1922), not assigned(onyx, 1921).
:- assigned(ryan, 1923), not assigned(onyx, 1922).
:- assigned(ryan, 1924), not assigned(onyx, 1923).

% Yoshio is not assigned
:- assigned(yoshio, _).

% Map the correct answer to option/1
% Option (A): Louis is not assigned to the project
option(a) :- not assigned(louis, _).

% Option (B): Ryan is not assigned to the project
option(b) :- not assigned(ryan, _).

% Option (C): Tiffany is not assigned to the project
option(c) :- not assigned(tiffany, _).

% Option (D): Onyx is assigned to 1922
option(d) :- assigned(onyx, 1922).

% Option (E): Louis is assigned to 1924
option(e) :- assigned(louis, 1924).

#show option/1.