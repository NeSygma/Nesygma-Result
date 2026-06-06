% Define the students and years
student(louis). student(mollie). student(onyx). student(ryan). student(tiffany). student(yoshio).
year(1921). year(1922). year(1923). year(1924).

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

% Yoshio is not assigned to the project
:- assigned(_, yoshio).

% Define the answer choices as possible conditions
% (A) Louis is not assigned to the project.
answer_a :- not assigned(_, louis).

% (B) Ryan is not assigned to the project.
answer_b :- not assigned(_, ryan).

% (C) Tiffany is not assigned to the project.
answer_c :- not assigned(_, tiffany).

% (D) Onyx is assigned to 1922.
answer_d :- assigned(1922, onyx).

% (E) Louis is assigned to 1924.
answer_e :- assigned(1924, louis).

% Map the correct answer to option/1
option(a) :- answer_a.
option(b) :- answer_b.
option(c) :- answer_c.
option(d) :- answer_d.
option(e) :- answer_e.

#show option/1.