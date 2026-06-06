% Students and Days
student(grecia; hakeem; joe; katya; louise).
day(1..5).
shift(1; 2).

% Each student works exactly 2 shifts
2 { assign(S, D, Sh) : day(D), shift(Sh) } 2 :- student(S).

% Each shift is worked by exactly one student
1 { assign(S, D, Sh) : student(S) } 1 :- day(D), shift(Sh).

% No student works both shifts of any day
:- assign(S, D, 1), assign(S, D, 2).

% Louise works the second shift on two consecutive days
louise_second(D) :- assign(louise, D, 2).
count_louise_second(N) :- N = #count { D : louise_second(D) }.
:- count_louise_second(N), N != 2.

% Exactly one pair of consecutive days
consecutive_pair(D) :- louise_second(D), louise_second(D+1).
count_consecutive(N) :- N = #count { D : consecutive_pair(D) }.
:- count_consecutive(N), N != 1.

% Grecia works the first shift on two nonconsecutive days
grecia_first(D) :- assign(grecia, D, 1).
count_grecia_first(N) :- N = #count { D : grecia_first(D) }.
:- count_grecia_first(N), N != 2.
:- grecia_first(D), grecia_first(D+1).

% Katya works on Tuesday (2) and Friday (5)
1 { assign(katya, 2, S) : shift(S) } 1.
1 { assign(katya, 5, S) : shift(S) } 1.

% Hakeem and Joe work on the same day at least once
same_day(D) :- assign(hakeem, D, _), assign(joe, D, _).
count_same_day(N) :- N = #count { D : same_day(D) }.
:- count_same_day(N), N < 1.

% Grecia and Louise never work on the same day
:- assign(grecia, D, _), assign(louise, D, _).

% The question provided is clearly mismatched (cookbooks vs art gallery).
% Since I cannot answer the multiple choice question as it is, 
% I will output a placeholder indicating the logic is sound.
#show solution_exists.
solution_exists :- assign(_,_,_).