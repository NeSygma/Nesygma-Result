% Define the days and sessions
% Days: Wednesday (wed), Thursday (thu), Friday (fri)
% Sessions: morning (morning), afternoon (afternoon)
day(wed; thu; fri).
session(morning; afternoon).

% Lab assistants
assistant(julio; kevin; lan; nessa; olivia; rebecca).

% Define the time slots (day + session)
time_slot(D, S) :- day(D), session(S).

% Assign each assistant to a unique time slot
1 { assigned(A, D, S) : time_slot(D, S) } 1 :- assistant(A).

% Ensure no two assistants are assigned to the same time slot
:- assigned(A1, D, S), assigned(A2, D, S), A1 != A2.

% Constraints:
% 1. Kevin and Rebecca must lead sessions on the same day
:- assigned(kevin, D1, _), assigned(rebecca, D2, _), D1 != D2.

% 2. Lan and Olivia cannot lead sessions on the same day
:- assigned(lan, D1, _), assigned(olivia, D2, _), D1 == D2.

% 3. Nessa must lead an afternoon session
:- assigned(nessa, _, S), S != afternoon.

% 4. Julio's session must meet on an earlier day than Olivia's
:- assigned(julio, D1, _), assigned(olivia, D2, _), D1 >= D2.

% Given condition: Julio leads the Thursday afternoon session
assigned(julio, thu, afternoon).

% Olivia must be on a later day than Julio, so Olivia must be on Friday
assigned(olivia, fri, S) :- session(S).

% Lan cannot be on the same day as Olivia (Friday), so Lan must be on Wednesday or Thursday
% Lan must be on morning session (since afternoon sessions are constrained)
assigned(lan, wed, morning).
assigned(lan, thu, morning).

% Nessa must be on an afternoon session. Possible days: Wednesday or Friday (since Thursday afternoon is taken by Julio)
assigned(nessa, wed, afternoon).
assigned(nessa, fri, afternoon).

% Kevin and Rebecca must be on the same day. Possible days: Wednesday or Friday (since Thursday morning is still open)
assigned(kevin, wed, S) :- session(S).
assigned(rebecca, wed, S) :- session(S).
assigned(kevin, fri, S) :- session(S).
assigned(rebecca, fri, S) :- session(S).

% Now, let's check for uniqueness

% Olivia is uniquely determined to be on Friday (day is fixed, session is not)
uniquely_determined(olivia) :- assigned(olivia, fri, _).

% Lan is uniquely determined to be on morning session (either Wednesday or Thursday)
uniquely_determined(lan) :- assigned(lan, _, morning).

% Nessa is not uniquely determined (can be Wednesday afternoon or Friday afternoon)

% Kevin and Rebecca are not uniquely determined (can be Wednesday or Friday)

% Count the number of uniquely determined assistants (excluding Julio)
num_uniquely_determined(N) :- N = #count { A : uniquely_determined(A), A != julio }.

% Map the correct answer to option/1
option(a) :- num_uniquely_determined(1).
option(b) :- num_uniquely_determined(2).
option(c) :- num_uniquely_determined(3).
option(d) :- num_uniquely_determined(4).
option(e) :- num_uniquely_determined(5).

#show option/1.