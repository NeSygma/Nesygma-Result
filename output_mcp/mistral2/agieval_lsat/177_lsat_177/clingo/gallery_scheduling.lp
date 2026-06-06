% Domain: Students and Days
student(grecia). student(hakeem). student(joe). student(katya). student(louise).
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).
shift(first). shift(second).

% Each student works exactly two shifts
1 { works(Student, Day, Shift) : day(Day), shift(Shift) } 2 :- student(Student).

% Each shift is worked by exactly one student
:- works(S1, D, Sh), works(S2, D, Sh), S1 != S2.

% No student works both shifts of any day
:- works(S, D, first), works(S, D, second).

% Louise works the second shift on two consecutive days
consecutive(D1, D2) :- day(D1), day(D2), D2 = D1 + 1.
:- { works(louise, D, second) : day(D) } 2, not two_consecutive_louise.
two_consecutive_louise :- consecutive(D1, D2), works(louise, D1, second), works(louise, D2, second).

% Grecia works the first shift on two nonconsecutive days
nonconsecutive(D1, D2) :- day(D1), day(D2), D1 != D2, not consecutive(D1, D2).
:- { works(grecia, D, first) : day(D) } 2, not two_nonconsecutive_grecia.
two_nonconsecutive_grecia :- nonconsecutive(D1, D2), works(grecia, D1, first), works(grecia, D2, first).

% Katya works on Tuesday and Friday
:- not works(katya, tuesday, _).
:- not works(katya, friday, _).

% Hakeem and Joe work on the same day at least once
:- not same_day_hakeem_joe.
same_day_hakeem_joe :- works(hakeem, D, _), works(joe, D, _).

% Grecia and Louise never work on the same day
grecia_day(D) :- works(grecia, D, _).
louise_day(D) :- works(louise, D, _).
:- grecia_day(D), louise_day(D).

% Hakeem works on Wednesday (given condition)
:- not works(hakeem, wednesday, _).

% Joe's working days (to be constrained by the answer choices)
% We will encode the answer choices as constraints and check which one holds.

% Define the answer choices as possible scenarios
% (A) Joe works on Monday and Wednesday
answer_a :- works(joe, monday, _), works(joe, wednesday, _).

% (B) Joe works on Monday and Thursday
answer_b :- works(joe, monday, _), works(joe, thursday, _).

% (C) Joe works on Tuesday and Wednesday
answer_c :- works(joe, tuesday, _), works(joe, wednesday, _).

% (D) Joe works on Tuesday and Thursday
answer_d :- works(joe, tuesday, _), works(joe, thursday, _).

% (E) Joe works on Wednesday and Thursday
answer_e :- works(joe, wednesday, _), works(joe, thursday, _).

% Only one answer can be correct
:- answer_a, answer_b.
:- answer_a, answer_c.
:- answer_a, answer_d.
:- answer_a, answer_e.
:- answer_b, answer_c.
:- answer_b, answer_d.
:- answer_b, answer_e.
:- answer_c, answer_d.
:- answer_c, answer_e.
:- answer_d, answer_e.

% Map the correct answer to option/1
option(a) :- answer_a.
option(b) :- answer_b.
option(c) :- answer_c.
option(d) :- answer_d.
option(e) :- answer_e.

#show option/1.