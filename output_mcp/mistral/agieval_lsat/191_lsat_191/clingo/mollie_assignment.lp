% Domains
year(1921..1924).
student(louis; mollie; onyx; ryan; tiffany; yoshio).

% Assignment: each year has exactly one student
1 { assigned(S, Y) : student(S) } 1 :- year(Y).

% Each student is assigned to at most one year
:- assigned(S, Y1), assigned(S, Y2), Y1 != Y2.

% Constraints
% 1. Only Louis or Tiffany can be assigned to 1923
:- assigned(S, 1923), S != louis, S != tiffany.

% 2. If Mollie is assigned, she must be in 1921 or 1922
:- assigned(mollie, Y), Y != 1921, Y != 1922.

% 3. If Tiffany is assigned, Ryan must be assigned
:- assigned(tiffany, _), not assigned(ryan, _).

% 4. If Ryan is assigned, Onyx must be in the year immediately prior
:- assigned(ryan, Y), not assigned(onyx, Y-1).

% For the question: We need to find which condition forces Mollie to be in 1922
% We'll test each option by adding it as a constraint and checking if it leads to
% assigned(mollie, 1922) being true in all answer sets

% Option A: Louis is assigned to 1924
% This doesn't directly constrain Mollie's assignment to 1922
option(a) :- assigned(louis, 1924), not -option(a), not -option(b), not -option(c), not -option(d), not -option(e).
-option(a) :- assigned(louis, 1924), assigned(mollie, Y), Y != 1922.

% Option B: Onyx is assigned to 1921
% This makes 1921 unavailable, so if Mollie is assigned, she must be in 1922
option(b) :- assigned(onyx, 1921), not -option(b), not -option(a), not -option(c), not -option(d), not -option(e).
-option(b) :- assigned(onyx, 1921), assigned(mollie, Y), Y != 1922.

% Option C: Onyx is assigned to 1924
% This doesn't directly constrain Mollie's assignment to 1922
option(c) :- assigned(onyx, 1924), not -option(c), not -option(a), not -option(b), not -option(d), not -option(e).
-option(c) :- assigned(onyx, 1924), assigned(mollie, Y), Y != 1922.

% Option D: Tiffany is assigned to 1923
% This forces Ryan to be assigned, which forces Onyx to be in prior year
% But this doesn't necessarily force Mollie to be in 1922
option(d) :- assigned(tiffany, 1923), not -option(d), not -option(a), not -option(b), not -option(c), not -option(e).
-option(d) :- assigned(tiffany, 1923), assigned(mollie, Y), Y != 1922.

% Option E: Yoshio is assigned to 1921
% This makes 1921 unavailable, similar to option B
option(e) :- assigned(yoshio, 1921), not -option(e), not -option(a), not -option(b), not -option(c), not -option(d).
-option(e) :- assigned(yoshio, 1921), assigned(mollie, Y), Y != 1922.

% Only one option can be correct
:- option(X), option(Y), X != Y.

% Show the correct option
#show option/1.