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
option(a) :- assigned(lan, wednesday, morning).

% Option B: Lan's session meets Thursday afternoon
option(b) :- assigned(lan, thursday, afternoon).

% Option C: Nessa's session meets Friday afternoon
option(c) :- assigned(nessa, friday, afternoon).

% Option D: Olivia's session meets Thursday morning
option(d) :- assigned(olivia, thursday, morning).

% Option E: Olivia's session meets Friday morning
option(e) :- assigned(olivia, friday, morning).

#show option/1.