% Domains
day(wednesday; thursday; friday).
time(morning; afternoon).
assistant(julio; kevin; lan; nessa; olivia; rebecca).

% Sessions are (day, time) pairs
session(D, T) :- day(D), time(T).

% Assign each assistant to exactly one session
1 { assigned(A, D, T) : session(D, T) } 1 :- assistant(A).

% Constraint 1: Kevin and Rebecca must lead sessions on the same day
:- assigned(kevin, D1, _), assigned(rebecca, D2, _), D1 != D2.

% Constraint 2: Lan and Olivia cannot lead sessions on the same day
:- assigned(lan, D1, _), assigned(olivia, D2, _), D1 == D2.

% Constraint 3: Nessa must lead an afternoon session
:- assigned(nessa, _, T), T != afternoon.

% Constraint 4: Julio's session must be on an earlier day than Olivia's
% Define day ordering: wednesday < thursday < friday
day_order(wednesday, 1).
day_order(thursday, 2).
day_order(friday, 3).

:- assigned(julio, D1, _), assigned(olivia, D2, _),
   day_order(D1, O1), day_order(D2, O2), O1 >= O2.

% Additional constraint from the question: Kevin's session is on the day before Nessa's
% This means Kevin's day is immediately before Nessa's day
day_before(wednesday, thursday).
day_before(thursday, friday).

:- assigned(kevin, D1, _), assigned(nessa, D2, _),
   not day_before(D1, D2).

% Define assistants assigned to Thursday afternoon in this model
thursday_afternoon_assistant(A) :- assigned(A, thursday, afternoon).

% Define the set of all possible assistants who could be assigned to Thursday afternoon in any model
% We will use a choice rule to collect all such assistants
{ possible_thursday_afternoon_assistant(A) : assistant(A) }.

% Ensure that possible_thursday_afternoon_assistant(A) is true if A is assigned to Thursday afternoon in any model
% This is tricky in ASP, so we will instead derive the correct option based on the possible assignments

% For the multiple choice, we need to determine which option is correct
% The question asks: which one of the following is a complete and accurate list of lab assistants any one of whom could lead the Thursday afternoon session?

% This means we need to find all assistants A such that there exists a valid assignment where A is assigned to Thursday afternoon

% Let's define the options as sets
option(a) :- possible_thursday_afternoon_assistant(julio),
             possible_thursday_afternoon_assistant(nessa),
             not possible_thursday_afternoon_assistant(kevin),
             not possible_thursday_afternoon_assistant(rebecca),
             not possible_thursday_afternoon_assistant(lan),
             not possible_thursday_afternoon_assistant(olivia).

option(b) :- possible_thursday_afternoon_assistant(kevin),
             possible_thursday_afternoon_assistant(rebecca),
             not possible_thursday_afternoon_assistant(julio),
             not possible_thursday_afternoon_assistant(lan),
             not possible_thursday_afternoon_assistant(nessa),
             not possible_thursday_afternoon_assistant(olivia).

option(c) :- possible_thursday_afternoon_assistant(kevin),
             possible_thursday_afternoon_assistant(nessa),
             possible_thursday_afternoon_assistant(rebecca),
             not possible_thursday_afternoon_assistant(julio),
             not possible_thursday_afternoon_assistant(lan),
             not possible_thursday_afternoon_assistant(olivia).

option(d) :- possible_thursday_afternoon_assistant(julio),
             possible_thursday_afternoon_assistant(kevin),
             possible_thursday_afternoon_assistant(nessa),
             possible_thursday_afternoon_assistant(rebecca),
             not possible_thursday_afternoon_assistant(lan),
             not possible_thursday_afternoon_assistant(olivia).

option(e) :- possible_thursday_afternoon_assistant(julio),
             possible_thursday_afternoon_assistant(kevin),
             possible_thursday_afternoon_assistant(lan),
             possible_thursday_afternoon_assistant(nessa),
             possible_thursday_afternoon_assistant(rebecca),
             not possible_thursday_afternoon_assistant(olivia).

#show option/1.
#show thursday_afternoon_assistant/1.
#show possible_thursday_afternoon_assistant/1.