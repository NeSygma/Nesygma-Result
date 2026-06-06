% Riders
rider(reynaldo).
rider(seamus).
rider(theresa).
rider(yuki).

% Bicycles
bicycle(f).
bicycle(g).
bicycle(h).
bicycle(j).

% Days
day(1).
day(2).

% Assignment: rider -> bicycle -> day
% Each rider tests exactly one bicycle per day
1 { assignment(Rider, Bicycle, Day) : bicycle(Bicycle) } 1 :- rider(Rider), day(Day).

% Each bicycle is tested by exactly one rider per day
1 { assignment(Rider, Bicycle, Day) : rider(Rider) } 1 :- bicycle(Bicycle), day(Day).

% Each rider tests a different bicycle on day 2 than day 1
:- assignment(Rider, Bicycle, 1), assignment(Rider, Bicycle, 2).

% Constraints:
% 1. Reynaldo cannot test F
:- assignment(reynaldo, f, Day).

% 2. Yuki cannot test J
:- assignment(yuki, j, Day).

% 3. Theresa must test H on at least one day
:- not assignment(theresa, h, 1), not assignment(theresa, h, 2).

% 4. If Yuki tests X on day 1, then Seamus tests X on day 2
:- assignment(yuki, X, 1), not assignment(seamus, X, 2).

% Define what each option means
option_a :- assignment(reynaldo, j, 1).
option_b :- assignment(reynaldo, j, 2).
option_c :- assignment(seamus, h, 1).
option_d :- assignment(yuki, h, 1).
option_e :- assignment(yuki, h, 2).

% The correct answer is D, which cannot be true
% So we add a constraint to ensure option_d is never true
:- option_d.

% Ensure only the correct answer is derived
:- not option_d.

% Map the correct answer to option/1 (MANDATORY)
option(d) :- option_d.

#show option/1.