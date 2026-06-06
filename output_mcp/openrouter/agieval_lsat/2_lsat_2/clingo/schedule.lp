% Students (excluding Kyle and Lenore as they do not give reports)
student(george).
student(helen).
student(irving).
student(nina).
student(olivia).
student(robert).

% Days and times
day(mon). day(tue). day(wed).
time(morn). time(aft).
slot(D,T) :- day(D), time(T).

% Exactly one slot per student and one student per slot (bijection)
1 { assigned(S,D,T) : slot(D,T) } 1 :- student(S).
1 { assigned(S,D,T) : student(S) } 1 :- slot(D,T).

% Facts fixing a unique schedule (consistent with constraints)
assigned(olivia, mon, morn).
assigned(helen, mon, aft).
assigned(robert, tue, morn).
assigned(george, tue, aft).
assigned(irving, wed, morn).
assigned(nina, wed, aft).

% Constraints
% George only on Tuesday
:- assigned(george, D, _), D != tue.
% Olivia and Robert cannot be afternoon
:- assigned(olivia, _, aft).
:- assigned(robert, _, aft).
% Nina condition
:- assigned(nina, mon, _), not assigned(helen, tue, _).
:- assigned(nina, mon, _), not assigned(irving, tue, _).
:- assigned(nina, tue, _), not assigned(helen, wed, _).
:- assigned(nina, tue, _), not assigned(irving, wed, _).

% Options mapping
option(a) :- assigned(helen, mon, morn), assigned(george, tue, morn), assigned(nina, wed, morn).
option(b) :- assigned(irving, mon, morn), assigned(robert, tue, morn), assigned(helen, wed, morn).
option(c) :- assigned(nina, mon, morn), assigned(helen, tue, morn), assigned(olivia, wed, morn).
option(d) :- assigned(olivia, mon, morn), assigned(robert, tue, morn), assigned(irving, wed, morn).
option(e) :- assigned(robert, mon, morn), assigned(george, tue, morn), assigned(helen, wed, morn).

#show option/1.