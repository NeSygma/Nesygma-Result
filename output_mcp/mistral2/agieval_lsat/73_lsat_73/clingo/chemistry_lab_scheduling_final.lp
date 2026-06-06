% Define the days and sessions
% Days: Wednesday, Thursday, Friday
% Sessions: Morning, Afternoon

% Lab assistants: Julio, Kevin, Lan, Nessa, Olivia, Rebecca

% Days and sessions as constants
day(wednesday). day(thursday). day(friday).
session(morning). session(afternoon).

% Lab assistants
assistant(julio). assistant(kevin). assistant(lan). assistant(nessa). assistant(olivia). assistant(rebecca).

% Assign each session a day and a session type
% We have 6 sessions: 3 days * 2 sessions/day
% Represent sessions as day-session pairs
1 { assigned_day_session(D, S) : day(D), session(S) } 6.

% Each assistant leads exactly one session
1 { assigned_assistant(A, D, S) : assistant(A) } 1 :- assigned_day_session(D, S).

% Constraints:

% 1. Kevin and Rebecca must lead sessions on the same day
:- assigned_assistant(kevin, D1, _), assigned_assistant(rebecca, D2, _), D1 != D2.

% 2. Lan and Olivia cannot lead sessions on the same day
:- assigned_assistant(lan, D1, _), assigned_assistant(olivia, D2, _), D1 == D2.

% 3. Nessa must lead an afternoon session
:- assigned_assistant(nessa, _, S), session(S), S != afternoon.

% 4. Julio's session must meet on an earlier day than Olivia's
:- assigned_assistant(julio, D1, _), assigned_assistant(olivia, D2, _), day(D1), day(D2), D1 >= D2.

% Additional constraint: If Kevin's session meets on the day before Nessa's
% This means: D_kevin = D_nessa - 1 (in terms of day order)

% Define day order
next_day(wednesday, thursday).
next_day(thursday, friday).

% Constraint: Kevin's day is the day before Nessa's
:- assigned_assistant(kevin, D_kevin, _), assigned_assistant(nessa, D_nessa, _), 
    not next_day(D_kevin, D_nessa).

% Define the Thursday afternoon session
assigned_assistant(A, thursday, afternoon) :- assigned_assistant(A, thursday, afternoon).

% Now, derive the possible assistants for Thursday afternoon session
% We will map the answer choices based on the valid assignments

% Option A: Julio, Nessa
option(a) :-
    assigned_assistant(julio, thursday, afternoon),
    assigned_assistant(nessa, thursday, afternoon),
    not assigned_assistant(kevin, thursday, afternoon),
    not assigned_assistant(lan, thursday, afternoon),
    not assigned_assistant(olivia, thursday, afternoon),
    not assigned_assistant(rebecca, thursday, afternoon).

% Option B: Kevin, Rebecca
option(b) :-
    assigned_assistant(kevin, thursday, afternoon),
    assigned_assistant(rebecca, thursday, afternoon),
    not assigned_assistant(julio, thursday, afternoon),
    not assigned_assistant(lan, thursday, afternoon),
    not assigned_assistant(olivia, thursday, afternoon),
    not assigned_assistant(nessa, thursday, afternoon).

% Option C: Kevin, Nessa, Rebecca
option(c) :-
    assigned_assistant(kevin, thursday, afternoon),
    assigned_assistant(nessa, thursday, afternoon),
    assigned_assistant(rebecca, thursday, afternoon),
    not assigned_assistant(julio, thursday, afternoon),
    not assigned_assistant(lan, thursday, afternoon),
    not assigned_assistant(olivia, thursday, afternoon).

% Option D: Julio, Kevin, Nessa, Rebecca
option(d) :-
    assigned_assistant(julio, thursday, afternoon),
    assigned_assistant(kevin, thursday, afternoon),
    assigned_assistant(nessa, thursday, afternoon),
    assigned_assistant(rebecca, thursday, afternoon),
    not assigned_assistant(lan, thursday, afternoon),
    not assigned_assistant(olivia, thursday, afternoon).

% Option E: Julio, Kevin, Lan, Nessa, Rebecca
option(e) :-
    assigned_assistant(julio, thursday, afternoon),
    assigned_assistant(kevin, thursday, afternoon),
    assigned_assistant(lan, thursday, afternoon),
    assigned_assistant(nessa, thursday, afternoon),
    assigned_assistant(rebecca, thursday, afternoon),
    not assigned_assistant(olivia, thursday, afternoon).

#show option/1.