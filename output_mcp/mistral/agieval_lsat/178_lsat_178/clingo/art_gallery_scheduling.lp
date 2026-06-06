% Domains with numbering for arithmetic
% Days: 0=monday, 1=tuesday, 2=wednesday, 3=thursday, 4=friday

% Base facts for days and their numeric indices
day(0, monday).
day(1, tuesday).
day(2, wednesday).
day(3, thursday).
day(4, friday).

% Students and shifts
student(grecia; hakeem; joe; katya; louise).
shift(first; second).

% Katya works on Tuesday and Friday (at least one shift per day, not both)
1 { works(katya, 1, SH) : shift(SH) } 1.
1 { works(katya, 4, SH) : shift(SH) } 1.

% Each student works exactly 2 shifts
2 { works(S, D, SH) : day(D, _), shift(SH) } 2 :- student(S).

% No student works both shifts of any day
:- works(S, D, first), works(S, D, second).

% Grecia and Louise never work on the same day
:- works(grecia, D, _), works(louise, D, _).

% Hakeem and Joe work on the same day at least once
same_day(S1, S2, D) :- works(S1, D, _), works(S2, D, _), S1 != S2.
:- student(S1), student(S2), S1 = hakeem, S2 = joe, not same_day(hakeem, joe, _).

% Grecia and Joe both work on at least one day
grecia_and_joe_same_day :- works(grecia, D, _), works(joe, D, _).
:- not grecia_and_joe_same_day.

% Louise works second shift on exactly two consecutive days
% Define consecutive days
consecutive(D, D+1) :- day(D, _), day(D+1, _).

% Count the number of consecutive day pairs where Louise works second shift
louise_second_consecutive(D, D+1) :- consecutive(D, D+1), works(louise, D, second), works(louise, D+1, second).

% Louise must work second shift on exactly two consecutive days
% This means exactly one pair of consecutive days
:- 1 != #count { D : louise_second_consecutive(D, D+1) }.

% Grecia works first shift on exactly two nonconsecutive days
% Define nonconsecutive days (not adjacent)
nonconsecutive(D1, D2) :- day(D1, _), day(D2, _), D1 < D2, not consecutive(D1, D2).

% Count the number of nonconsecutive day pairs where Grecia works first shift
grecia_first_nonconsecutive(D1, D2) :- nonconsecutive(D1, D2), works(grecia, D1, first), works(grecia, D2, first).

% Grecia must work first shift on exactly two nonconsecutive days
:- 2 != #count { D1, D2 : grecia_first_nonconsecutive(D1, D2) }.

% Map the correct answer to option/1
% Option A: Grecia works the first shift on Tuesday (day 1)
option(a) :- works(grecia, 1, first).

% Option B: Hakeem works the second shift on Monday (day 0)
option(b) :- works(hakeem, 0, second).

% Option C: Hakeem works the second shift on Wednesday (day 2)
option(c) :- works(hakeem, 2, second).

% Option D: Joe works the first shift on Wednesday (day 2)
option(d) :- works(joe, 2, first).

% Option E: Joe works the first shift on Thursday (day 3)
option(e) :- works(joe, 3, first).

#show option/1.