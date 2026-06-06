% Domains
student(grecia). student(hakeem). student(joe). student(katya). student(louise).
day(mon). day(tue). day(wed). day(thu). day(fri).
shift(first). shift(second).

% Consecutive day pairs
consecutive(mon, tue). consecutive(tue, wed). consecutive(wed, thu). consecutive(thu, fri).

% Each shift is worked by exactly one student
1 { works(S, D, Sh) : student(S) } 1 :- day(D), shift(Sh).

% Each student works exactly 2 shifts
2 { works(S, D, Sh) : day(D), shift(Sh) } 2 :- student(S).

% Constraint 3: No student works both shifts of any day
:- works(S, D, first), works(S, D, second).

% Constraint 4: Louise works second shift on two consecutive days
louise_consec(D1, D2) :- consecutive(D1, D2), works(louise, D1, second), works(louise, D2, second).
:- not louise_consec(_, _).

% Constraint 5: Grecia works first shift on exactly 2 nonconsecutive days
grecia_first(D) :- works(grecia, D, first).
2 { grecia_first(D) : day(D) } 2.
:- grecia_first(D1), grecia_first(D2), consecutive(D1, D2).
:- grecia_first(D1), grecia_first(D2), consecutive(D2, D1).

% Constraint 6: Katya works on Tuesday and Friday (one shift each)
katya_on(D) :- works(katya, D, first).
katya_on(D) :- works(katya, D, second).
:- not katya_on(tue).
:- not katya_on(fri).

% Constraint 7: Hakeem and Joe work on the same day at least once
hj_same(D) :- works(hakeem, D, Sh1), works(joe, D, Sh2).
:- not hj_same(_).

% Constraint 8: Grecia and Louise never work on the same day
:- works(grecia, D, Sh1), works(louise, D, Sh2).

% Constraint 9: At least one day where Grecia and Joe both work
gj_same(D) :- works(grecia, D, Sh1), works(joe, D, Sh2).
:- not gj_same(_).

% Answer choices evaluation
cond_a :- works(grecia, tue, first).
cond_b :- works(hakeem, mon, second).
cond_c :- works(hakeem, wed, second).
cond_d :- works(joe, wed, first).
cond_e :- works(joe, thu, first).

option(a) :- cond_a.
option(b) :- cond_b.
option(c) :- cond_c.
option(d) :- cond_d.
option(e) :- cond_e.

#show option/1.
#show works/3.