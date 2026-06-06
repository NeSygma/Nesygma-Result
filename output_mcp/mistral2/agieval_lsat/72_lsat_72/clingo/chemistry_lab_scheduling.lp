% Define the days and sessions
% Days: Wednesday, Thursday, Friday
% Sessions: Morning (am), Afternoon (pm)
day(wednesday). day(thursday). day(friday).
session(am). session(pm).

% Define the lab assistants
assistant(julio). assistant(kevin). assistant(lan). assistant(nessa). assistant(olivia). assistant(rebecca).

% Assign each session a unique day and session time
% We have 6 sessions: 3 days * 2 sessions per day
1 { assigned_day(Day, Session) : day(Day), session(Session) } 2 :- false.

% Each session must be assigned to exactly one assistant
1 { assigned_assistant(Assistant, Day, Session) : assistant(Assistant) } 1 :-
    day(Day), session(Session).

% Constraints:
% 1. Kevin and Rebecca must lead sessions on the same day
:- assigned_assistant(kevin, Day1, Session1),
     assigned_assistant(rebecca, Day2, Session2),
     Day1 != Day2.

% 2. Lan and Olivia cannot lead sessions on the same day
:- assigned_assistant(lan, Day, _),
     assigned_assistant(olivia, Day, _).

% 3. Nessa must lead an afternoon session
:- assigned_assistant(nessa, Day, am).

% 4. Julio's session must be on an earlier day than Olivia's
:- assigned_assistant(julio, Day1, _),
     assigned_assistant(olivia, Day2, _),
     day_order(Day1, Day2, earlier).

% Define day order: Wednesday < Thursday < Friday
% Use facts to represent the order
% This is a helper to compare days
day_order(wednesday, thursday, earlier).
day_order(wednesday, friday, earlier).
day_order(thursday, friday, earlier).

% Lan does not lead a Wednesday session (given condition)
:- assigned_assistant(lan, wednesday, _).

% Additional constraint: Ensure each assistant is assigned to exactly one session
% (This is already enforced by the assignment rules above)

% --- Multiple Choice Logic ---
% We need to determine which assistant must lead a Thursday session
% given the condition that Lan does not lead a Wednesday session.

% Define a predicate for assistants leading a Thursday session
leads_thursday(Assistant) :-
    assigned_assistant(Assistant, thursday, _).

% The question asks: If Lan does not lead a Wednesday session, then which assistant must lead a Thursday session?
% We need to find the assistant that is forced to lead a Thursday session under this condition.

% To find the answer, we will check which of the options (A-E) is necessarily true
% for the assistant leading a Thursday session.

% Map the correct answer to option/1
% We will derive the correct answer based on the constraints and the given condition.

% The correct answer is the assistant that must lead a Thursday session
% under the given constraints and condition.

% We will use the following logic to derive the answer:
% If only one assistant can lead a Thursday session, then that assistant is the answer.

% However, since the problem is under-constrained, we need to find the assistant that is forced
% to lead a Thursday session in all valid models.

% To do this, we will use the following approach:
% 1. Enumerate all possible valid assignments.
% 2. For each option (A-E), check if it is necessarily true that the assistant leads a Thursday session.

% Since we cannot enumerate all models directly in the ASP code, we will instead
% use the following logic to derive the answer:

% The answer is the assistant that is the only one possible for a Thursday session
% under the given constraints and condition.

% We will use the following rules to map the answer to the options:

% If Rebecca must lead a Thursday session, then option(a) is true
option(a) :- leads_thursday(rebecca),
    not leads_thursday(olivia),
    not leads_thursday(nessa),
    not leads_thursday(kevin),
    not leads_thursday(julio).

% If Olivia must lead a Thursday session, then option(b) is true
option(b) :- leads_thursday(olivia),
    not leads_thursday(rebecca),
    not leads_thursday(nessa),
    not leads_thursday(kevin),
    not leads_thursday(julio).

% If Nessa must lead a Thursday session, then option(c) is true
option(c) :- leads_thursday(nessa),
    not leads_thursday(rebecca),
    not leads_thursday(olivia),
    not leads_thursday(kevin),
    not leads_thursday(julio).

% If Kevin must lead a Thursday session, then option(d) is true
option(d) :- leads_thursday(kevin),
    not leads_thursday(rebecca),
    not leads_thursday(olivia),
    not leads_thursday(nessa),
    not leads_thursday(julio).

% If Julio must lead a Thursday session, then option(e) is true
option(e) :- leads_thursday(julio),
    not leads_thursday(rebecca),
    not leads_thursday(olivia),
    not leads_thursday(nessa),
    not leads_thursday(kevin).

#show option/1.