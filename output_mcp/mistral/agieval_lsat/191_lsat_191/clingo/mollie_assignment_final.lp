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

% Base scenario: Mollie is assigned to 1922
% We want to find which condition forces this to be true

% Option A: Louis is assigned to 1924
% This doesn't force Mollie to be in 1922
option_a :- assigned(louis, 1924).

% Option B: Onyx is assigned to 1921
% This forces 1921 to be taken, so Mollie must be in 1922
option_b :- assigned(onyx, 1921).

% Option C: Onyx is assigned to 1924
% This doesn't force Mollie to be in 1922
option_c :- assigned(onyx, 1924).

% Option D: Tiffany is assigned to 1923
% This forces Ryan to be assigned, which forces Onyx to be in 1922
% But doesn't directly force Mollie to be in 1922
option_d :- assigned(tiffany, 1923).

% Option E: Yoshio is assigned to 1921
% This forces 1921 to be taken, so Mollie must be in 1922
option_e :- assigned(yoshio, 1921).

% The correct answer is the option that, when true, forces Mollie to be in 1922
% We check which options are consistent with Mollie being in 1922

% If an option is true and Mollie is in 1922, it's a candidate
candidate(a) :- option_a, assigned(mollie, 1922).
candidate(b) :- option_b, assigned(mollie, 1922).
candidate(c) :- option_c, assigned(mollie, 1922).
candidate(d) :- option_d, assigned(mollie, 1922).
candidate(e) :- option_e, assigned(mollie, 1922).

% Only one option can be the correct answer
1 { answer(X) : candidate(X) } 1.

% Show the answer
#show answer/1.