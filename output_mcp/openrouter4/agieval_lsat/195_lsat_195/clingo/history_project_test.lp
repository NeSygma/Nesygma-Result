% Students
student(luis; mollie; onyx; ryan; tiffany; yoshio).
% Years
year(1921; 1922; 1923; 1924).

% Exactly one student per year
1 { assigned(S, Y) : student(S) } 1 :- year(Y).

% Each student at most one year
:- assigned(S, Y1), assigned(S, Y2), Y1 != Y2.

% Condition 1: Only Louis or Tiffany can be assigned to 1923
:- assigned(S, 1923), S != luis, S != tiffany.

% Condition 2: If Mollie is assigned, she must be 1921 or 1922
:- assigned(mollie, Y), Y != 1921, Y != 1922.

% Condition 3: If Tiffany is assigned, Ryan must be assigned
ryan_assigned :- assigned(ryan, _).
:- assigned(tiffany, _), not ryan_assigned.

% Condition 4: If Ryan is assigned, Onyx must be immediately prior to Ryan
previous(1922, 1921). previous(1923, 1922). previous(1924, 1923).
:- assigned(ryan, 1921).
:- assigned(ryan, Y), previous(Y, Yprev), not assigned(onyx, Yprev).

% Test which student can be in 1922
{ try(S) : student(S) }.
:- #count { S : try(S) } != 1.
assigned(S, 1922) :- try(S).

% Show results
#show try/1.
#show assigned/2.