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
assigned_thursday_afternoon(A) :- assigned_assistant(A, thursday, afternoon).

% Now, derive the possible assistants for Thursday afternoon session
% We will map the answer choices based on the valid assignments

% Option A: Julio, Nessa
option(a) :-
    assigned_thursday_afternoon(julio),
    assigned_thursday_afternoon(nessa),
    not assigned_thursday_afternoon(kevin),
    not assigned_thursday_afternoon(lan),
    not assigned_thursday_afternoon(olivia),
    not assigned_thursday_afternoon(rebecca).

% Option B: Kevin, Rebecca
option(b) :-
    assigned_thursday_afternoon(kevin),
    assigned_thursday_afternoon(rebecca),
    not assigned_thursday_afternoon(julio),
    not assigned_thursday_afternoon(lan),
    not assigned_thursday_afternoon(olivia),
    not assigned_thursday_afternoon(nessa).

% Option C: Kevin, Nessa, Rebecca
option(c) :-
    assigned_thursday_afternoon(kevin),
    assigned_thursday_afternoon(nessa),
    assigned_thursday_afternoon(rebecca),
    not assigned_thursday_afternoon(julio),
    not assigned_thursday_afternoon(lan),
    not assigned_thursday_afternoon(olivia).

% Option D: Julio, Kevin, Nessa, Rebecca
option(d) :-
    assigned_thursday_afternoon(julio),
    assigned_thursday_afternoon(kevin),
    assigned_thursday_afternoon(nessa),
    assigned_thursday_afternoon(rebecca),
    not assigned_thursday_afternoon(lan),
    not assigned_thursday_afternoon(olivia).

% Option E: Julio, Kevin, Lan, Nessa, Rebecca
option(e) :-
    assigned_thursday_afternoon(julio),
    assigned_thursday_afternoon(kevin),
    assigned_thursday_afternoon(lan),
    assigned_thursday_afternoon(nessa),
    assigned_thursday_afternoon(rebecca),
    not assigned_thursday_afternoon(olivia).

#show option/1.