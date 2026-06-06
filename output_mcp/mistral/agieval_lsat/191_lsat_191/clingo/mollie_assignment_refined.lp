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


% --- Define the options as scenarios ---

% Option A: Louis is assigned to 1924
% We force this condition and see if Mollie must be in 1922
% If there exists a model where Louis is in 1924 and Mollie is not in 1922, then A is not the answer
scenario_a :- assigned(louis, 1924).

% Option B: Onyx is assigned to 1921
% If Onyx is in 1921, then 1921 is taken, so Mollie must be in 1922
scenario_b :- assigned(onyx, 1921).

% Option C: Onyx is assigned to 1924
% If Onyx is in 1924, then 1924 is taken, but Mollie could still be in 1921 or 1922
scenario_c :- assigned(onyx, 1924).

% Option D: Tiffany is assigned to 1923
% If Tiffany is in 1923, then Ryan must be assigned (constraint 3)
% If Ryan is assigned, Onyx must be in the year prior (constraint 4)
% So Onyx must be in 1922
% This doesn't force Mollie to be in 1922
scenario_d :- assigned(tiffany, 1923).

% Option E: Yoshio is assigned to 1921
% If Yoshio is in 1921, then 1921 is taken, so Mollie must be in 1922
scenario_e :- assigned(yoshio, 1921).


% --- Check if Mollie must be in 1922 in each scenario ---

% For each scenario, check if Mollie is in 1922
mollie_in_1922 :- assigned(mollie, 1922).

% For each scenario, check if Mollie is NOT in 1922
mollie_not_in_1922 :- assigned(mollie, 1921).

% --- Determine which scenario forces Mollie to be in 1922 ---

% If scenario_b is true, then Mollie must be in 1922 (because 1921 is taken by Onyx)
% So if scenario_b is true, then mollie_in_1922 must be true
% If there is a model where scenario_b is true and mollie_not_in_1922 is true, then scenario_b does not force Mollie to be in 1922

% We want to find the scenario where:
% - The scenario is true
% - Mollie is in 1922
% - There is no model where the scenario is true and Mollie is not in 1922

% To encode this, we will use the following logic:
% For each scenario, if the scenario is true, then Mollie must be in 1922
% We will derive answer(X) for the scenario that satisfies this

% If scenario_b is true, then Mollie must be in 1922
answer(b) :- scenario_b, mollie_in_1922.

% If scenario_e is true, then Mollie must be in 1922
answer(e) :- scenario_e, mollie_in_1922.

% If scenario_a is true, Mollie does not have to be in 1922
% So we do not derive answer(a)

% If scenario_c is true, Mollie does not have to be in 1922
% So we do not derive answer(c)

% If scenario_d is true, Mollie does not have to be in 1922
% So we do not derive answer(d)

% Only one answer can be correct
1 { correct_answer(X) : answer(X) } 1 :- answer(X).

% Show the correct answer
#show correct_answer/1.