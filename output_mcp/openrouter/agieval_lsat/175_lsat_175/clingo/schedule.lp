% Domains
day(1..5).
student(grecia). student(hakeem). student(joe). student(katya). student(louise).

% Second shift definitions per option
second_shift_a(1,hakeem). second_shift_a(2,louise). second_shift_a(3,louise). second_shift_a(4,hakeem). second_shift_a(5,katya).
second_shift_b(1,joe). second_shift_b(2,hakeem). second_shift_b(3,grecia). second_shift_b(4,louise). second_shift_b(5,louise).
second_shift_c(1,joe). second_shift_c(2,katya). second_shift_c(3,hakeem). second_shift_c(4,louise). second_shift_c(5,katya).
second_shift_d(1,louise). second_shift_d(2,katya). second_shift_d(3,joe). second_shift_d(4,louise). second_shift_d(5,katya).
second_shift_e(1,louise). second_shift_e(2,louise). second_shift_e(3,hakeem). second_shift_e(4,joe). second_shift_e(5,joe).

% Choose exactly one option
1 { option_selected(a); option_selected(b); option_selected(c); option_selected(d); option_selected(e) } 1.

% Map selected option to concrete second_shift facts
second_shift(D,S) :- option_selected(a), second_shift_a(D,S).
second_shift(D,S) :- option_selected(b), second_shift_b(D,S).
second_shift(D,S) :- option_selected(c), second_shift_c(D,S).
second_shift(D,S) :- option_selected(d), second_shift_d(D,S).
second_shift(D,S) :- option_selected(e), second_shift_e(D,S).

% Each day must have a second shift (provided by option)
:- day(D), not second_shift(D,_).

% First shift: exactly one student per day, different from second shift
1 { first_shift(D,S) : student(S), not second_shift(D,S) } 1 :- day(D).

% Each student works exactly two shifts total (first + second)
:- student(S), #count{ D : first_shift(D,S) ; second_shift(D,S) } != 2.

% Katya works on Tuesday (day 2) and Friday (day 5) (either shift)
% No Katya on other days
:- day(D), D != 2, D != 5, (first_shift(D,katya); second_shift(D,katya)).
% Must appear on day 2 and day 5
:- not first_shift(2,katya), not second_shift(2,katya).
:- not first_shift(5,katya), not second_shift(5,katya).

% Louise works second shift on exactly two consecutive days and nowhere else
:- #count{ D : second_shift(D,louise) } != 2.
% Ensure the two days are consecutive
consecutive_louise :- second_shift(D,louise), second_shift(D2,louise), D2 = D+1, day(D), day(D2).
:- not consecutive_louise.
% Louise cannot work first shift
:- first_shift(D,louise).

% Grecia works first shift on exactly two nonconsecutive days, never second, never same day as Louise
:- second_shift(_,grecia).
:- #count{ D : first_shift(D,grecia) } != 2.
% No consecutive days for Grecia
:- first_shift(D,grecia), first_shift(D2,grecia), D2 = D+1, day(D), day(D2).
% Grecia and Louise never on same day
:- first_shift(D,grecia), second_shift(D,louise).

% Hakeem and Joe share a day (one first, one second) at least once
shared_day :- first_shift(D,hakeem), second_shift(D,joe).
shared_day :- first_shift(D,joe), second_shift(D,hakeem).
:- not shared_day.

% Map option to output
option(a) :- option_selected(a).
option(b) :- option_selected(b).
option(c) :- option_selected(c).
option(d) :- option_selected(d).
option(e) :- option_selected(e).

#show option/1.