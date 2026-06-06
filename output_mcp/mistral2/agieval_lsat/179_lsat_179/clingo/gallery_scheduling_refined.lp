% Domain: Students and Days
student(grecia). student(hakeem). student(joe). student(katya). student(louise).
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).
shift(first). shift(second).

% Each student works exactly two shifts
1 { works(S, D, Sh) : day(D), shift(Sh) } 2 :- student(S).

% Each shift is worked by exactly one student
1 { works(S, D, Sh) : student(S) } 1 :- day(D), shift(Sh).

% No student works both shifts of any day
:- works(S, D, first), works(S, D, second).

% On at least two consecutive days, Louise works the second shift
consecutive(D1, D2) :- day(D1), day(D2), D2 = D1 + 1.
:- consecutive(D1, D2), not works(louise, D2, second), louise_consecutive_count(N), N < 2.
louise_consecutive_count(N) :- N = #count { D : consecutive(D1, D), works(louise, D, second) }.

% On at least two nonconsecutive days, Grecia works the first shift
nonconsecutive(D1, D2) :- day(D1), day(D2), D1 != D2, not consecutive(D1, D2).
:- nonconsecutive(D1, D2), not works(grecia, D1, first), not works(grecia, D2, first), grecia_nonconsecutive_count(N), N < 2.
grecia_nonconsecutive_count(N) :- N = #count { D : nonconsecutive(D1, D), works(grecia, D, first) }.

% Katya works on Tuesday and Friday
:- not works(katya, tuesday, _).
:- not works(katya, friday, _).

% Hakeem and Joe work on the same day at least once
:- not same_day(hakeem, joe).
same_day(S1, S2) :- student(S1), student(S2), S1 != S2, day(D), works(S1, D, _), works(S2, D, _).

% Grecia and Louise never work on the same day
grecia_louise_same_day :- day(D), works(grecia, D, _), works(louise, D, _).
:- grecia_louise_same_day.

% Katya works the second shift on Tuesday (given condition)
:- not works(katya, tuesday, second).

% --- Multiple Choice Options ---
% (A) Grecia works the first shift on Monday
option(a) :- works(grecia, monday, first).

% (B) Hakeem works the first shift on Monday
option(b) :- works(hakeem, monday, first).

% (C) Hakeem works the second shift on Wednesday
option(c) :- works(hakeem, wednesday, second).

% (D) Joe works the second shift on Thursday
option(d) :- works(joe, thursday, second).

% (E) Louise works the second shift on Monday
option(e) :- works(louise, monday, second).

#show option/1.