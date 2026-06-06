% Domains
day(wed; thu; fri).
time(am; pm).
session(D, T) :- day(D), time(T).

assistant(julio; kevin; lan; nessa; olivia; rebecca).

day_order(wed,0; thu,1; fri,2).

% For each assistant, we test if they can be Thursday PM
% We use a choice rule to pick one test at a time
test_assistant(julio; kevin; lan; nessa; olivia; rebecca).

% Exactly one test per run
1 { test(A) : test_assistant(A) } 1.

% If we test A, then A is assigned to Thursday PM
assign(A, thu, pm) :- test(A).

% Each other session gets exactly one assistant
1 { assign(A, D, T) : assistant(A) } 1 :- session(D, T), not (D = thu, T = pm).

% Each assistant assigned to exactly one session
:- assistant(A), not 1 { assign(A, D, T) : session(D, T) } 1.

% ----- Constraints -----

% 1. Kevin and Rebecca same day
:- assign(kevin, D1, _), assign(rebecca, D2, _), D1 != D2.

% 2. Lan and Olivia cannot be same day
:- assign(lan, D, _), assign(olivia, D, _).

% 3. Nessa must lead afternoon session
:- assign(nessa, _, am).

% 4. Julio earlier day than Olivia
:- assign(julio, D1, _), assign(olivia, D2, _), day_order(D1, O1), day_order(D2, O2), O1 >= O2.

% 5. Kevin's session meets on the day before Nessa's
:- assign(kevin, D1, _), assign(nessa, D2, _), day_order(D1, O1), day_order(D2, O2), O1 + 1 != O2.

% ----- Determine which assistants can be Thursday PM -----
% If test(A) is true and we found a solution, then A is possible
possible_thu_pm(A) :- test(A).

#show possible_thu_pm/1.
#show assign/3.