% Domain: students and years
student(louis).
student(mollie).
student(onyx).
student(ryan).
student(tiffany).
student(yoshio).

% Years available for assignment
year(1921).
year(1922).
year(1923).
year(1924).

% Each year must be assigned exactly one student
1 { assigned(S, Y) : student(S) } 1 :- year(Y).

% Each student can be assigned to at most one year
:- assigned(S1, Y), assigned(S2, Y), S1 != S2.

% Only Louis or Tiffany can be assigned to 1923
:- assigned(S, 1923), S != louis, S != tiffany.

% If Mollie is assigned, she must be assigned to 1921 or 1922
:- assigned(mollie, Y), Y != 1921, Y != 1922.

% If Tiffany is assigned, then Ryan must be assigned
:- assigned(tiffany, _), not assigned(ryan, _).

% If Ryan is assigned, then Onyx must be assigned to the year immediately prior to Ryan's
:- assigned(ryan, Y), not assigned(onyx, Y-1).

% Helper to check if a student is assigned to a year
is_assigned(S, Y) :- assigned(S, Y).

% --- Multiple Choice Logic ---

% Condition for A: Louis is assigned to 1924
option(a) :- assigned(louis, 1924).

% Condition for B: Onyx is assigned to 1921
option(b) :- assigned(onyx, 1921).

% Condition for C: Onyx is assigned to 1924
option(c) :- assigned(onyx, 1924).

% Condition for D: Tiffany is assigned to 1923
option(d) :- assigned(tiffany, 1923).

% Condition for E: Yoshio is assigned to 1921
option(e) :- assigned(yoshio, 1921).

#show option/1.