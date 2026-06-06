% Domains
student(grecia). student(hakeem). student(joe). student(katya). student(louise).

day(1..5). % 1=Mon,2=Tue,3=Wed,4=Thu,5=Fri
shift(first). shift(second).

% Helper predicate for work day
works_day(S,D) :- assign(S,D,_).

% Each student works exactly two shifts (on distinct days, not both shifts same day)
2 { assign(S,D,Sh) : day(D), shift(Sh) } 2 :- student(S).
:- assign(S,D,first), assign(S,D,second).

% Each shift per day is assigned to exactly one student
1 { assign(S,D,Sh) : student(S) } 1 :- day(D), shift(Sh).

% Katya works on Tuesday (2) and Friday (5)
:- not works_day(katya,2).
:- not works_day(katya,5).

% Louise works second shift on two consecutive days, never first shift
:- assign(louise, D, first).
2 { assign(louise, D, second) : day(D) } 2.
% enforce consecutiveness (must be consecutive days)
:- assign(louise, D1, second), assign(louise, D2, second), D1 != D2, D2 != D1+1, D1 != D2+1.

% Grecia works first shift on two nonconsecutive days, never second shift
:- assign(grecia, D, second).
2 { assign(grecia, D, first) : day(D) } 2.
% enforce non-consecutive (no consecutive days)
:- assign(grecia, D1, first), assign(grecia, D2, first), D1 != D2, D2 = D1+1.

% Hakeem and Joe work on the same day at least once
same_day(D) :- assign(hakeem, D, _), assign(joe, D, _).
:- not same_day(_).

% Grecia and Louise never work on the same day
:- assign(grecia, D, _), assign(louise, D, _).

% Hakeem works on Wednesday (day 3)
:- not assign(hakeem, 3, _).

% Options for Joe's days (exactly two days)
option(a) :- works_day(joe,1), works_day(joe,3).
option(b) :- works_day(joe,1), works_day(joe,4).
option(c) :- works_day(joe,2), works_day(joe,3).
option(d) :- works_day(joe,2), works_day(joe,4).
option(e) :- works_day(joe,3), works_day(joe,4).

#show option/1.