% Define the students and years
student(louis).
student(mollie).
student(onyx).
student(ryan).
student(tiffany).
student(yoshio).

% Define the years
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

% Define the possible assignments for 1922
possible_assignment_1922(louis).
possible_assignment_1922(mollie).
possible_assignment_1922(onyx).
possible_assignment_1922(ryan).
possible_assignment_1922(yoshio).

% Check if a student CANNOT be assigned to 1922
cannot_be_assigned_to_1922(S) :-
    student(S),
    not assigned(S, 1922),
    possible_assignment_1922(S).

% Map the correct answer to option/1
option(a) :- cannot_be_assigned_to_1922(louis).
option(b) :- cannot_be_assigned_to_1922(mollie).
option(c) :- cannot_be_assigned_to_1922(onyx).
option(d) :- cannot_be_assigned_to_1922(ryan).
option(e) :- cannot_be_assigned_to_1922(yoshio).

#show option/1.