% Students and Days
student(grecia). student(hakeem). student(joe). student(katya). student(louise).
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).
shift(first). shift(second).

% Time slots: each day has two shifts
time(D, S) :- day(D), shift(S).

% Each shift is worked by exactly one student
1 { works(Student, D, S) : student(Student) } 1 :- time(D, S).

% Each student works exactly two shifts total
2 { works(Student, D, S) : time(D, S) } 2 :- student(Student).

% Constraint 1: No student works both shifts of any day
:- works(Student, D, first), works(Student, D, second).

% Constraint 2: Louise works the second shift on two consecutive days
consecutive(monday, tuesday). consecutive(tuesday, wednesday).
consecutive(wednesday, thursday). consecutive(thursday, friday).

louise_consecutive :- works(louise, D1, second), works(louise, D2, second), consecutive(D1, D2).
:- not louise_consecutive.

% Constraint 3: Grecia works the first shift on two nonconsecutive days
nonconsecutive(D1, D2) :- day(D1), day(D2), D1 != D2, 
    not consecutive(D1, D2), not consecutive(D2, D1).
grecia_nonconsecutive :- works(grecia, D1, first), works(grecia, D2, first), nonconsecutive(D1, D2).
:- not grecia_nonconsecutive.

% Constraint 4: Katya works on Tuesday and Friday
katya_tuesday :- works(katya, tuesday, _).
katya_friday :- works(katya, friday, _).
:- not katya_tuesday, not katya_friday.

% Constraint 5: Hakeem and Joe work on the same day at least once
same_day_hj :- works(hakeem, D, _), works(joe, D, _).
:- not same_day_hj.

% Constraint 6: Grecia and Louise never work on the same day
:- works(grecia, D, _), works(louise, D, _).

% Additional condition: At least one day where both Grecia and Joe work
grecia_joe_same_day :- works(grecia, D, _), works(joe, D, _).
:- not grecia_joe_same_day.

% Let's add more constraints to reduce possibilities
% Since Louise works second shift on two consecutive days, and Grecia and Louise never work same day,
% Grecia cannot work on those days when Louise works second shift.

% Let's enumerate possible consecutive pairs for Louise
louise_pair(D1, D2) :- works(louise, D1, second), works(louise, D2, second), consecutive(D1, D2).

% Grecia cannot work on D1 or D2 if Louise works second shift there
:- works(grecia, D, _), louise_pair(D1, D2), (D = D1; D = D2).

% Now evaluate the answer choices
% (A) Grecia works the first shift on Tuesday
option(a) :- works(grecia, tuesday, first).

% (B) Hakeem works the second shift on Monday
option(b) :- works(hakeem, monday, second).

% (C) Hakeem works the second shift on Wednesday
option(c) :- works(hakeem, wednesday, second).

% (D) Joe works the first shift on Wednesday
option(d) :- works(joe, wednesday, first).

% (E) Joe works the first shift on Thursday
option(e) :- works(joe, thursday, first).

#show option/1.

% Generate all possible models to see which options can be true
#show.