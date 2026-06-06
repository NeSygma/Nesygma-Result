% Base facts about students, days, and shifts
student(grecia).
student(hakeem).
student(joe).
student(katya).
student(louise).

day(monday).
day(tuesday).
day(wednesday).
day(thursday).
day(friday).

shift(first).
shift(second).

% Each student works exactly two shifts
1 { works(S, D, Sh) : day(D), shift(Sh) } 2 :- student(S).

% Each shift is worked by exactly one student
1 { works(S, D, Sh) : student(S) } 1 :- day(D), shift(Sh).

% No student works both shifts of any day
:- works(S, D, first), works(S, D, second).

% Louise works the second shift on two consecutive days
consecutive(D1, D2) :- day(D1), day(D2), D2 = D1 + 1.
:- works(louise, D1, second), works(louise, D2, second), not consecutive(D1, D2).

% Grecia works the first shift on two nonconsecutive days
nonconsecutive(D1, D2) :- day(D1), day(D2), D1 != D2, not consecutive(D1, D2).
:- works(grecia, D1, first), works(grecia, D2, first), not nonconsecutive(D1, D2).

% Katya works on Tuesday and Friday
:- not works(katya, tuesday, _).
:- not works(katya, friday, _).

% Hakeem and Joe work on the same day at least once
hakeem_joe_same_day :- works(hakeem, D, _), works(joe, D, _).
:- not hakeem_joe_same_day.

% Grecia and Louise never work on the same day
grecia_louise_same_day :- works(grecia, D, _), works(louise, D, _).
:- grecia_louise_same_day.

% If there is at least one day on which Grecia and Joe both work at the gallery
% (i.e., Grecia and Joe work on the same day, regardless of shift)
grecia_joe_same_day :- works(grecia, D, _), works(joe, D, _).

% --- Multiple Choice Options ---
% (A) Grecia works the first shift on Tuesday.
option(a) :- works(grecia, tuesday, first).

% (B) Hakeem works the second shift on Monday.
option(b) :- works(hakeem, monday, second).

% (C) Hakeem works the second shift on Wednesday.
option(c) :- works(hakeem, wednesday, second).

% (D) Joe works the first shift on Wednesday.
option(d) :- works(joe, wednesday, first).

% (E) Joe works the first shift on Thursday.
option(e) :- works(joe, thursday, first).

#show option/1.