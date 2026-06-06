% Domains
day(1..5).
shift(first;second).
student(grecia;hakeem;joe;katya;louise).

% Exactly one student per shift
1 { work(S,D,Sh) : student(S) } 1 :- day(D), shift(Sh).

% Each student works exactly two shifts
:- student(S), #count { D,Sh : work(S,D,Sh) } != 2.

% No student works both shifts of any day
:- work(S,D,first), work(S,D,second).

% Louise works second shift on exactly two consecutive days, only second shifts
:- work(louise,_,first).
:- #count { D : work(louise,D,second) } != 2.
% enforce consecutiveness
consecutive_louise :- work(louise,D,second), work(louise,D1,second), D1 = D+1.
:- not consecutive_louise.

% Grecia works first shift on exactly two nonconsecutive days, only first shifts
:- work(grecia,_,second).
:- #count { D : work(grecia,D,first) } != 2.
% forbid consecutive days for Grecia
:- work(grecia,D,first), work(grecia,D1,first), D1 = D+1.

% Katya works on Tuesday (2) and Friday (5) (any shift)
:- not work(katya,2,first), not work(katya,2,second).
:- not work(katya,5,first), not work(katya,5,second).
% Katya does not work other days
:- work(katya,D,_), D != 2, D != 5.

% Hakeem and Joe share a day at least once
shared_day(D) :- work(hakeem,D,_), work(joe,D,_).
:- not shared_day(_).

% Grecia and Louise never same day
:- work(grecia,D,_), work(louise,D,_).

% Additional condition: at least one day where Grecia and Joe both work
shared_gj(D) :- work(grecia,D,_), work(joe,D,_).
:- not shared_gj(_).

% Options conditions
option(a) :- work(grecia,2,first).
option(b) :- work(hakeem,1,second).
option(c) :- work(hakeem,3,second).
option(d) :- work(joe,3,first).
option(e) :- work(joe,4,first).

% Exactly one option must hold
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.