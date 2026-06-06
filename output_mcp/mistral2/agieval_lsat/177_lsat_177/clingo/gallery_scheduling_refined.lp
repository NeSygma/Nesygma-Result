% Domain: Students and Days
student(grecia). student(hakeem). student(joe). student(katya). student(louise).
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).
shift(first). shift(second).

% Consecutive days
consecutive(monday, tuesday).
consecutive(tuesday, wednesday).
consecutive(wednesday, thursday).
consecutive(thursday, friday).

% Nonconsecutive days
nonconsecutive(D1, D2) :- day(D1), day(D2), D1 != D2, not consecutive(D1, D2).

% Each student works exactly two shifts
1 { works(Student, Day, Shift) : day(Day), shift(Shift) } 2 :- student(Student).

% Each shift is worked by exactly one student
:- works(S1, D, Sh), works(S2, D, Sh), S1 != S2.

% No student works both shifts of any day
:- works(S, D, first), works(S, D, second).

% Louise works the second shift on two consecutive days
:- { works(louise, D, second) : day(D) } < 2.
:- works(louise, D1, second), works(louise, D2, second), not consecutive(D1, D2).

% Grecia works the first shift on two nonconsecutive days
:- { works(grecia, D, first) : day(D) } < 2.
:- works(grecia, D1, first), works(grecia, D2, first), not nonconsecutive(D1, D2).

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

% Map the correct answer to option/1
option(a) :- answer_a, not answer_b, not answer_c, not answer_d, not answer_e.
option(b) :- answer_b, not answer_a, not answer_c, not answer_d, not answer_e.
option(c) :- answer_c, not answer_a, not answer_b, not answer_d, not answer_e.
option(d) :- answer_d, not answer_a, not answer_b, not answer_c, not answer_e.
option(e) :- answer_e, not answer_a, not answer_b, not answer_c, not answer_d.

#show option/1.