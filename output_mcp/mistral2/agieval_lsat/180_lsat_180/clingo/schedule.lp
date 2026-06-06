% Define the days and shifts
day(1..5). % Monday (1) to Friday (5)
shift(first; second).

% Define the students
student(grecia; hakeem; joe; katya; louise).

% Each student works exactly two shifts
1 { works(S, D, Sh) : day(D), shift(Sh) } 2 :- student(S).

% Each shift is worked by exactly one student
:- day(D), shift(Sh), not 1 { works(S, D, Sh) : student(S) } 1.

% No student works both shifts of any day
:- student(S), day(D), shift(Sh1), shift(Sh2), Sh1 != Sh2, works(S, D, Sh1), works(S, D, Sh2).

% Louise works the second shift on at least two consecutive days
consecutive_louise_days(D) :-
    day(D), day(D+1), works(louise, D, second), works(louise, D+1, second).
:- { consecutive_louise_days(D) } < 2.

% Grecia works the first shift on at least two nonconsecutive days
nonconsecutive_grecia_days(D1, D2) :-
    day(D1), day(D2), D1 < D2, D2 - D1 > 1, works(grecia, D1, first), works(grecia, D2, first).
:- { nonconsecutive_grecia_days(D1, D2) } < 2.

% Katya works on Tuesday (2) and Friday (5)
:- not works(katya, 2, _).
:- not works(katya, 5, _).

% Hakeem and Joe work on the same day at least once
same_day_hakeem_joe :- day(D), works(hakeem, D, _), works(joe, D, _).
:- not same_day_hakeem_joe.

% Grecia and Louise never work on the same day
:- day(D), works(grecia, D, _), works(louise, D, _).

% --- Show the schedule for inspection ---
#show works/3.