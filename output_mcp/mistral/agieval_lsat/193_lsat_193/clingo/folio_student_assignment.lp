% Define students and years
student(louis; mollie; onyx; ryan; tiffany; yoshio).
year(1921; 1922; 1923; 1924).

% Define prior_year relationship
prior_year(1921, 1922).
prior_year(1922, 1923).
prior_year(1923, 1924).

% Each year has exactly one student
1 { assigned(S, Y) : student(S) } 1 :- year(Y).

% Constraint 1: Only Louis or Tiffany can be assigned to 1923
:- assigned(S, 1923), S != louis, S != tiffany.

% Constraint 2: If Mollie is assigned, she must be assigned to 1921 or 1922
:- assigned(mollie, Y), Y != 1921, Y != 1922.

% Constraint 3: If Tiffany is assigned, Ryan must be assigned
:- assigned(tiffany, _), not assigned(ryan, _).

% Constraint 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior
:- assigned(ryan, Y), not assigned(onyx, Y1) : prior_year(Y1, Y).

% Students who cannot be assigned to 1921
% Ryan cannot be assigned to 1921 because it would require Onyx in year 1920 (which doesn't exist)
cannot_be_assigned_to_1921(ryan).

% Count the number of students who could be assigned to 1921
% This is total_students - students_who_cannot_be_assigned_to_1921
count_possible(5) :- #count { S : student(S), not cannot_be_assigned_to_1921(S) } = 5.

% Map the count to the answer choices
option(a) :- count_possible(6).
option(b) :- count_possible(5).
option(c) :- count_possible(4).
option(d) :- count_possible(3).
option(e) :- count_possible(2).

#show option/1.