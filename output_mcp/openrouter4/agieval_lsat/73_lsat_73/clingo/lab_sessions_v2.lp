% Domains
day(wed; thu; fri).
time(am; pm).
session(D, T) :- day(D), time(T).

assistant(julio; kevin; lan; nessa; olivia; rebecca).

day_order(wed,0; thu,1; fri,2).

% Each session gets exactly one assistant
1 { assign(A, D, T) : assistant(A) } 1 :- session(D, T).

% Each assistant assigned to exactly one session
1 { assign(A, D, T) : session(D, T) } 1 :- assistant(A).

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

% ----- Check who can be Thursday PM -----
% An assistant is possible for Thursday PM if there is a valid assignment with them there
possible_thu_pm(A) :- assign(A, thu, pm).

#show possible_thu_pm/1.