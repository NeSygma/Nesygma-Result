%% Students, Days, Shifts
student(grecia; hakeem; joe; katya; louise).
day(mon; tue; wed; thu; fri).
shift(first; second).

%% Consecutive day pairs
consecutive(mon, tue).
consecutive(tue, wed).
consecutive(wed, thu).
consecutive(thu, fri).

%% Nonconsecutive day pairs
nonconsecutive(D1, D2) :- day(D1), day(D2), D1 != D2, not consecutive(D1, D2), not consecutive(D2, D1).

%% Each shift is worked by exactly one student
1 { works(S, D, Sh) : student(S) } 1 :- day(D), shift(Sh).

%% Each student works exactly two shifts total
:- student(S), not #count { D, Sh : works(S, D, Sh) } = 2.

%% No student works both shifts of any day
:- works(S, D, first), works(S, D, second).

%% Constraint 1: On two consecutive days, Louise works the second shift
satisfied_louise_consecutive :- consecutive(D1, D2), works(louise, D1, second), works(louise, D2, second).
:- not satisfied_louise_consecutive.

%% Constraint 2: On two nonconsecutive days, Grecia works the first shift
satisfied_grecia_nonconsecutive :- nonconsecutive(D1, D2), works(grecia, D1, first), works(grecia, D2, first).
:- not satisfied_grecia_nonconsecutive.

%% Constraint 3: Katya works on Tuesday and Friday
katya_tue :- works(katya, tue, _).
katya_fri :- works(katya, fri, _).
:- not katya_tue.
:- not katya_fri.

%% Constraint 4: Hakeem and Joe work on the same day at least once
hakeem_joe_same_day :- works(hakeem, D, _), works(joe, D, _).
:- not hakeem_joe_same_day.

%% Constraint 5: Grecia and Louise never work on the same day
:- works(grecia, D, _), works(louise, D, _).

%% TEST: Hakeem works on Wednesday (would make option B false)
hakeem_works_wed :- works(hakeem, wed, _).
:- not hakeem_works_wed.

#show works/3.