% Students and days
student(grecia). student(hakeem). student(joe). student(katya). student(louise).
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).
shift(first). shift(second).

% Time slots: each day has two shifts
time(D, S) :- day(D), shift(S).

% Each shift is worked by exactly one student
1 { works(Student, D, S) : student(Student) } 1 :- time(D, S).

% Each student works exactly two shifts total
2 { works(Student, D, S) : time(D, S) } 2 :- student(Student).

% No student works both shifts of any day
:- works(Student, D, first), works(Student, D, second).

% Louise works the second shift on two consecutive days
consecutive_days(monday, tuesday).
consecutive_days(tuesday, wednesday).
consecutive_days(wednesday, thursday).
consecutive_days(thursday, friday).
louise_consecutive :- works(louise, D1, second), works(louise, D2, second), consecutive_days(D1, D2).
:- not louise_consecutive.

% Grecia works the first shift on two nonconsecutive days
nonconsecutive_days(D1, D2) :- day(D1), day(D2), D1 != D2, 
    not consecutive_days(D1, D2), not consecutive_days(D2, D1).
grecia_nonconsecutive :- works(grecia, D1, first), works(grecia, D2, first), nonconsecutive_days(D1, D2).
:- not grecia_nonconsecutive.

% Katya works on Tuesday and Friday
katya_tuesday :- works(katya, tuesday, _).
katya_friday :- works(katya, friday, _).
:- not katya_tuesday, not katya_friday.

% Additional condition: Katya works the second shift on Tuesday
katya_tuesday_second :- works(katya, tuesday, second).
:- not katya_tuesday_second.

% Hakeem and Joe work on the same day at least once
same_day_hj :- works(hakeem, D, _), works(joe, D, _).
:- not same_day_hj.

% Grecia and Louise never work on the same day
:- works(grecia, D, _), works(louise, D, _).

% Now evaluate the options
% Option A: Grecia works the first shift on Monday
option_a :- works(grecia, monday, first).

% Option B: Hakeem works the first shift on Monday
option_b :- works(hakeem, monday, first).

% Option C: Hakeem works the second shift on Wednesday
option_c :- works(hakeem, wednesday, second).

% Option D: Joe works the second shift on Thursday
option_d :- works(joe, thursday, second).

% Option E: Louise works the second shift on Monday
option_e :- works(louise, monday, second).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.