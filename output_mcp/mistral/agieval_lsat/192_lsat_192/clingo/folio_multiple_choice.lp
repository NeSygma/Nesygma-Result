% Domains
student(louis; mollie; onyx; ryan; tiffany; yoshio).
year(1921; 1922; 1923; 1924).

% Assignment relation
% Ensure every student is assigned to at most one year
1 { assigned(S, Y) : year(Y) } 1 :- student(S).

% Each year has exactly one student
1 { assigned(S, Y) : student(S) } 1 :- year(Y).

% Only Louis or Tiffany can be assigned to 1923
:- assigned(S, 1923), S != louis, S != tiffany.

% If Mollie is assigned, she must be assigned to 1921 or 1922
:- assigned(mollie, Y), Y != 1921, Y != 1922.

% If Tiffany is assigned, Ryan must be assigned
:- assigned(tiffany, _), not assigned(ryan, _).

% If Ryan is assigned, Onyx must be assigned to the year immediately prior (if it exists)
:- assigned(ryan, Y), Y > 1921, not assigned(onyx, Y-1).

% Given: Both Ryan and Yoshio are assigned
:- not assigned(ryan, _).
:- not assigned(yoshio, _).

% Map the correct answer to option/1
% Option A: Louis is assigned to 1923
option(a) :- assigned(louis, 1923).

% Option B: Mollie is assigned to 1921
option(b) :- assigned(mollie, 1921).

% Option C: Onyx is assigned to 1922
option(c) :- assigned(onyx, 1922).

% Option D: Tiffany is assigned to 1924
option(d) :- assigned(tiffany, 1924).

% Option E: Yoshio is assigned to 1922
option(e) :- assigned(yoshio, 1922).

#show option/1.