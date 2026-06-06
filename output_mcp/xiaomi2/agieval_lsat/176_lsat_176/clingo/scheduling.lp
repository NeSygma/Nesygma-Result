% Domains
day(mon). day(tue). day(wed). day(thu). day(fri).
shift(first). shift(second).
student(grecia). student(hakeem). student(joe). student(katya). student(louise).

% Consecutive days (symmetric)
next_day(mon, tue). next_day(tue, wed). next_day(wed, thu). next_day(thu, fri).
consecutive(D1, D2) :- next_day(D1, D2).
consecutive(D1, D2) :- next_day(D2, D1).

% Helper: student works on a day (any shift)
works_on_day(S, D) :- works(S, D, first).
works_on_day(S, D) :- works(S, D, second).

% Each shift has exactly one student
1 { works(S, D, F) : student(S) } 1 :- day(D), shift(F).

% Each student works exactly 2 shifts
2 { works(S, D, F) : day(D), shift(F) } 2 :- student(S).

% No student works both shifts of any day
:- works(S, D, first), works(S, D, second).

% Grecia only works first shifts (derived from "two nonconsecutive days, first shift" + exactly 2 shifts)
:- works(grecia, _, second).

% Louise only works second shifts (derived from "two consecutive days, second shift" + exactly 2 shifts)
:- works(louise, _, first).

% Louise works second shift on two consecutive days
has_louise_consecutive :- works(louise, D1, second), works(louise, D2, second), consecutive(D1, D2).
:- not has_louise_consecutive.

% Grecia works first shift on two nonconsecutive days
has_grecia_nonconsecutive :- works(grecia, D1, first), works(grecia, D2, first), D1 != D2, not consecutive(D1, D2).
:- not has_grecia_nonconsecutive.

% Katya works on Tuesday and Friday (exactly one shift each, since total=2)
1 { works(katya, tue, F) : shift(F) } 1.
1 { works(katya, fri, F) : shift(F) } 1.
:- works(katya, D, _), D != tue, D != fri.

% Hakeem and Joe work on the same day at least once
same_day_hj :- works_on_day(hakeem, D), works_on_day(joe, D).
:- not same_day_hj.

% Grecia and Louise never work on the same day
:- works_on_day(grecia, D), works_on_day(louise, D).

% Answer options - check which must hold in ALL valid schedules
holds_a :- not works_on_day(grecia, tue).
holds_b :- not works_on_day(hakeem, wed).
holds_c :- not works_on_day(joe, tue).
holds_d :- not works_on_day(joe, thu).
holds_e :- not works_on_day(louise, tue).

option(a) :- holds_a.
option(b) :- holds_b.
option(c) :- holds_c.
option(d) :- holds_d.
option(e) :- holds_e.

#show works/3.
#show option/1.