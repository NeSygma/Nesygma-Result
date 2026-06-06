% Base facts: riders, bicycles, and days
rider(reynaldo; seamus; theresa; yuki).
bicycle(f; g; h; j).
day(1; 2).

% Assignments: assign(Rider, Bicycle, Day)
% We use a choice rule to allow assignments to be made
{ assign(Rider, Bicycle, Day) : bicycle(Bicycle) } = 1 :- rider(Rider), day(Day).

% Constraints:
% 1. Reynaldo cannot test F
:- assign(reynaldo, f, Day), day(Day).

% 2. Yuki cannot test J
:- assign(yuki, j, Day), day(Day).

% 3. Theresa must test H on at least one day
:- not assign(theresa, h, Day), day(Day).

% 4. The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
:- assign(yuki, Bicycle, 1), not assign(seamus, Bicycle, 2).

% Additional constraints to ensure all bicycles are tested each day
:- bicycle(Bicycle), day(Day), not assign(Rider, Bicycle, Day).

% Ensure each rider tests only one bicycle per day
:- rider(Rider), day(Day), { assign(Rider, Bicycle, Day) } != 1.

% Ensure each rider tests a different bicycle on the second day
:- rider(Rider), assign(Rider, B1, 1), assign(Rider, B2, 2), B1 = B2.

% Given condition: Theresa tests G on the second day
:- not assign(theresa, g, 2).

% Map the correct answer to option/1
% (A) Reynaldo tests H on the first day
option(a) :- assign(reynaldo, h, 1).

% (B) Reynaldo tests J on the first day
option(b) :- assign(reynaldo, j, 1).

% (C) Theresa tests H on the second day
option(c) :- assign(theresa, h, 2).

% (D) Theresa tests J on the first day
option(d) :- assign(theresa, j, 1).

% (E) Yuki tests H on the second day
option(e) :- assign(yuki, h, 2).

#show option/1.