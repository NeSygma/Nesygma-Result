% Students available
student(luis; mollie; onyx; ryan; tiffany; yoshio).

% Years
year(1921; 1922; 1923; 1924).

% Each year gets exactly one student assigned
1 { assigned(S, Y) : student(S) } 1 :- year(Y).

% Each student can be assigned to at most one year
:- student(S), #count{ Y : assigned(S, Y) } > 1.

% Condition: Only Louis or Tiffany can be assigned to 1923.
:- assigned(S, 1923), S != luis, S != tiffany.

% Condition: If Mollie is assigned to the project, then she must be assigned to either 1921 or 1922.
:- assigned(mollie, Y), Y != 1921, Y != 1922.

% Condition: If Tiffany is assigned to the project, then Ryan must be assigned to the project.
:- assigned(tiffany, _), not assigned(ryan, _).

% Condition: If Ryan is assigned to the project, then Onyx must be assigned to the year immediately prior to Ryan's.
:- assigned(ryan, Y), not assigned(onyx, Y - 1).

% Now determine which students CAN be assigned to 1922.
% A student CAN be assigned to 1922 if there exists some valid assignment where they are assigned to 1922.
can_be_1922(S) :- student(S), assigned(S, 1922).

% A student CANNOT be assigned to 1922 if they never appear in 1922 in any valid model.
% We'll use a different approach: check each option individually.

% Let's find all possible assignments and see who can be in 1922
#show assigned/2.