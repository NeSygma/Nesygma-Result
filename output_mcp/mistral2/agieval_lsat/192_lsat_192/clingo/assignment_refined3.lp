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
1 { assigned(Y, S) : student(S) } 1 :- year(Y).

% Each student can be assigned to at most one year
:- assigned(Y1, S), assigned(Y2, S), Y1 != Y2.

% Only Louis or Tiffany can be assigned to 1923
:- assigned(1923, S), S != louis, S != tiffany.

% If Mollie is assigned, she must be assigned to 1921 or 1922
:- assigned(Y, mollie), Y != 1921, Y != 1922.

% If Tiffany is assigned, then Ryan must be assigned
:- assigned(Y, tiffany), not assigned(_, ryan).

% If Ryan is assigned, then Onyx must be assigned to the year immediately prior to Ryan's
:- assigned(Y, ryan), not assigned(Y-1, onyx).

% Base condition: Both Ryan and Yoshio are assigned to the project
assigned(_, ryan).
assigned(_, yoshio).

% Additional constraint: Ensure all students are assigned to exactly one year
% (This is already implied by the first constraint, but we ensure no student is left out)

% Map the correct answer to option/1 (MANDATORY)
% (A) Louis is assigned to 1923
option(a) :- assigned(1923, louis).

% (B) Mollie is assigned to 1921
option(b) :- assigned(1921, mollie).

% (C) Onyx is assigned to 1922
option(c) :- assigned(1922, onyx).

% (D) Tiffany is assigned to 1924
option(d) :- assigned(1924, tiffany).

% (E) Yoshio is assigned to 1922
option(e) :- assigned(1922, yoshio).

#show option/1.