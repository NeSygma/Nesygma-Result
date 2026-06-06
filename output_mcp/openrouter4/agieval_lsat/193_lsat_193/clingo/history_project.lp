% Domain
student(louis; mollie; onyx; ryan; tiffany; yoshio).
year(1921; 1922; 1923; 1924).

% Choose exactly one student to test if they can be assigned to 1921
1 { test_1921(S) : student(S) } 1.

% If we are testing S, then S is assigned to 1921
assigned(S, 1921) :- test_1921(S).

% Assignment: each year gets exactly one student
1 { assigned(S, Y) : student(S) } 1 :- year(Y).

% A student cannot be assigned to two different years
:- assigned(S, Y1), assigned(S, Y2), Y1 != Y2.

% Condition 1: Only Louis or Tiffany can be assigned to 1923
:- assigned(S, 1923), S != louis, S != tiffany.

% Condition 2: If Mollie is assigned to the project, she must be 1921 or 1922
:- assigned(mollie, Y), Y != 1921, Y != 1922.

% Helper: a student is assigned to the project
assigned_to_project(S) :- assigned(S, _).

% Condition 3: If Tiffany is assigned, then Ryan must be assigned
:- assigned_to_project(tiffany), not assigned_to_project(ryan).

% Condition 4: If Ryan is assigned, then Onyx must be assigned
:- assigned_to_project(ryan), not assigned_to_project(onyx).

% Condition 4 continued: Onyx must be assigned to the year immediately prior to Ryan's
:- assigned(ryan, Y), assigned(onyx, Y2), Y2 != Y - 1.

% Derive which tested student can be assigned to 1921
possible_1921(S) :- test_1921(S).

#show possible_1921/1.