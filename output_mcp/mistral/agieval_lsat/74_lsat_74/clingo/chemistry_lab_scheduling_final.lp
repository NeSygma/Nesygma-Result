% Define the domain
 day(wednesday; thursday; friday).
time(morning; afternoon).
assistant(julio; kevin; lan; nessa; olivia; rebecca).

% Define day order for Julio < Olivia constraint
day_order(wednesday, thursday).
day_order(thursday, friday).
day_order(wednesday, friday).

% Base assignment: each assistant is assigned to exactly one session
{ assigned(A, D, T) : day(D), time(T) } 1 :- assistant(A).

% Each session has exactly one assistant
:- 2 { assigned(A, D, T) : assistant(A) }, day(D), time(T).

% Constraints:
% 1. Kevin and Rebecca must lead sessions on the same day
:- assigned(kevin, D1, _), assigned(rebecca, D2, _), D1 != D2.

% 2. Lan and Olivia cannot lead sessions on the same day
:- assigned(lan, D1, _), assigned(olivia, D2, _), D1 == D2.

% 3. Nessa must lead an afternoon session
:- assigned(nessa, _, morning).

% 4. Julio's session must be on an earlier day than Olivia's
:- assigned(julio, D1, _), assigned(olivia, D2, _), not day_order(D1, D2).

% Additional condition for this specific question: Julio and Kevin both lead morning sessions
:- not assigned(julio, _, morning).
:- not assigned(kevin, _, morning).

% Define what each option means:
% Option A: Lan's session meets Wednesday morning
% This is possible if we can assign lan to wednesday morning while satisfying all constraints
% We do not enforce it, but check if it is possible
possible_a :- assigned(lan, wednesday, morning).

% Option B: Lan's session meets Thursday afternoon
possible_b :- assigned(lan, thursday, afternoon).

% Option C: Nessa's session meets Friday afternoon
possible_c :- assigned(nessa, friday, afternoon).

% Option D: Olivia's session meets Thursday morning
possible_d :- assigned(olivia, thursday, morning).

% Option E: Olivia's session meets Friday morning
possible_e :- assigned(olivia, friday, morning).

% The correct answer is the option that is NOT possible, so it should not appear in any answer set
% We will show all possible options, and the one missing is the answer
option(a) :- possible_a, not excluded_a.
option(b) :- possible_b, not excluded_b.
option(c) :- possible_c, not excluded_c.
option(d) :- possible_d, not excluded_d.
option(e) :- possible_e, not excluded_e.

% Exclude options that are impossible under the constraints
% We need to ensure that the solver can derive excluded_X for options that are not possible
excluded_a :- not possible_a.
excluded_b :- not possible_b.
excluded_c :- not possible_c.
excluded_d :- not possible_d.
excluded_e :- not possible_e.

#show option/1.