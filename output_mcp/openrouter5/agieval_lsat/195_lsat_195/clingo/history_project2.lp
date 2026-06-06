% Students available
student(luis; mollie; onyx; ryan; tiffany; yoshio).

% Years
year(1921; 1922; 1923; 1924).

% Each year gets exactly one student assigned
1 { assigned(S, Y) : student(S) } 1 :- year(Y).

% Each student can be assigned to at most one year
:- student(S), 1 { assigned(S, Y) : year(Y) } > 1.

% Condition: Only Louis or Tiffany can be assigned to 1923.
:- assigned(S, 1923), S != luis, S != tiffany.

% Condition: If Mollie is assigned to the project, then she must be assigned to either 1921 or 1922.
:- assigned(mollie, Y), Y != 1921, Y != 1922.

% Condition: If Tiffany is assigned to the project, then Ryan must be assigned to the project.
:- assigned(tiffany, _), not assigned(ryan, _).

% Condition: If Ryan is assigned to the project, then Onyx must be assigned to the year immediately prior to Ryan's.
:- assigned(ryan, Y), not assigned(onyx, Y - 1).

% Now let's check each option systematically.
% We want to find which student CANNOT be assigned to 1922.
% We'll use a "test" approach: for each student, we force them to be assigned to 1922
% and see if the problem is satisfiable.

% Option A: Louis assigned to 1922
:- not option_a_possible.
option_a_possible :- assigned(luis, 1922).

% Option B: Mollie assigned to 1922
:- not option_b_possible.
option_b_possible :- assigned(mollie, 1922).

% Option C: Onyx assigned to 1922
:- not option_c_possible.
option_c_possible :- assigned(onyx, 1922).

% Option D: Ryan assigned to 1922
:- not option_d_possible.
option_d_possible :- assigned(ryan, 1922).

% Option E: Yoshio assigned to 1922
:- not option_e_possible.
option_e_possible :- assigned(yoshio, 1922).

% We need exactly one option to be impossible
% Let's just see all models and check manually
#show assigned/2.