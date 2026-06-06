% Domain: students and years
student(louis).
student(mollie).
student(onyx).
student(ryan).
student(tiffany).
student(yoshio).

% Years available for assignment
year(1921).
year(1922).
year(1923).
year(1924).

% Each year must be assigned exactly one student
1 { assigned(S, Y) : student(S) } 1 :- year(Y).

% Each student can be assigned to at most one year
:- assigned(S1, Y), assigned(S2, Y), S1 != S2.

% Only Louis or Tiffany can be assigned to 1923
:- assigned(S, 1923), S != louis, S != tiffany.

% If Mollie is assigned, she must be assigned to 1921 or 1922
:- assigned(mollie, Y), Y != 1921, Y != 1922.

% If Tiffany is assigned, then Ryan must be assigned
:- assigned(tiffany, _), not assigned(ryan, _).

% If Ryan is assigned, then Onyx must be assigned to the year immediately prior to Ryan's
:- assigned(ryan, Y), not assigned(onyx, Y-1).

% Helper to check if a student is assigned to a year
is_assigned(S, Y) :- assigned(S, Y).

% --- Multiple Choice Logic ---

% We need to determine for which condition Mollie must be assigned to 1922.
% We will check each condition individually and see if it forces Mollie to 1922.

% Let's define a predicate to check each condition and see if Mollie is forced to 1922.

% For each condition, we will:
% 1. Assume the condition is true.
% 2. Check if Mollie is assigned to 1922 in all valid assignments.
% 3. If yes, then the condition is the correct answer.

% We will use a choice rule to select which condition to check.
{ check_condition(A; B; C; D; E) } 1.

% Define the conditions
condition_a :- check_condition(a), assigned(louis, 1924).
condition_b :- check_condition(b), assigned(onyx, 1921).
condition_c :- check_condition(c), assigned(onyx, 1924).
condition_d :- check_condition(d), assigned(tiffany, 1923).
condition_e :- check_condition(e), assigned(yoshio, 1921).

% Check if Mollie is assigned to 1922
mollie_assigned_1922 :- assigned(mollie, 1922).

% If the condition forces Mollie to be assigned to 1922, then it is the correct answer.
correct_answer(a) :- condition_a, mollie_assigned_1922.
correct_answer(b) :- condition_b, mollie_assigned_1922.
correct_answer(c) :- condition_c, mollie_assigned_1922.
correct_answer(d) :- condition_d, mollie_assigned_1922.
correct_answer(e) :- condition_e, mollie_assigned_1922.

% Map the correct answer to option/1 (MANDATORY)
option(a) :- correct_answer(a).
option(b) :- correct_answer(b).
option(c) :- correct_answer(c).
option(d) :- correct_answer(d).
option(e) :- correct_answer(e).

#show option/1.