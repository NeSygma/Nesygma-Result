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
% We need to define an order for days: wednesday < thursday < friday

% Define day order
next_day(wednesday, thursday).
next_day(thursday, friday).

% Constraint: Kevin's day is the day before Nessa's
:- assigned_assistant(kevin, D_kevin, _), assigned_assistant(nessa, D_nessa, _), 
    not next_day(D_kevin, D_nessa).

% Query: Which assistants can lead the Thursday afternoon session?
% We need to find all possible assistants A such that:
% assigned_assistant(A, thursday, afternoon) is possible under the constraints.

% To answer the multiple-choice question, we need to check which options are possible.

% Define the possible assistants for Thursday afternoon session
possible_assistant_thu_afternoon(A) :-
    assigned_assistant(A, thursday, afternoon),
    assistant(A).

% Map the correct answer to option/1
% We need to check which options are fully covered by possible_assistant_thu_afternoon/1

% Option A: Julio, Nessa
option(a) :-
    possible_assistant_thu_afternoon(julio),
    possible_assistant_thu_afternoon(nessa),
    not possible_assistant_thu_afternoon(kevin),
    not possible_assistant_thu_afternoon(lan),
    not possible_assistant_thu_afternoon(olivia),
    not possible_assistant_thu_afternoon(rebecca).

% Option B: Kevin, Rebecca
option(b) :-
    possible_assistant_thu_afternoon(kevin),
    possible_assistant_thu_afternoon(rebecca),
    not possible_assistant_thu_afternoon(julio),
    not possible_assistant_thu_afternoon(lan),
    not possible_assistant_thu_afternoon(olivia),
    not possible_assistant_thu_afternoon(nessa).

% Option C: Kevin, Nessa, Rebecca
option(c) :-
    possible_assistant_thu_afternoon(kevin),
    possible_assistant_thu_afternoon(nessa),
    possible_assistant_thu_afternoon(rebecca),
    not possible_assistant_thu_afternoon(julio),
    not possible_assistant_thu_afternoon(lan),
    not possible_assistant_thu_afternoon(olivia).

% Option D: Julio, Kevin, Nessa, Rebecca
option(d) :-
    possible_assistant_thu_afternoon(julio),
    possible_assistant_thu_afternoon(kevin),
    possible_assistant_thu_afternoon(nessa),
    possible_assistant_thu_afternoon(rebecca),
    not possible_assistant_thu_afternoon(lan),
    not possible_assistant_thu_afternoon(olivia).

% Option E: Julio, Kevin, Lan, Nessa, Rebecca
option(e) :-
    possible_assistant_thu_afternoon(julio),
    possible_assistant_thu_afternoon(kevin),
    possible_assistant_thu_afternoon(lan),
    possible_assistant_thu_afternoon(nessa),
    possible_assistant_thu_afternoon(rebecca),
    not possible_assistant_thu_afternoon(olivia).

#show option/1.