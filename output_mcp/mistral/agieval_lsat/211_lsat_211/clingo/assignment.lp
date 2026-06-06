% Students
student(juana). student(kelly). student(lateefah). student(mei). student(olga).

% Teams
team(green). team(red).

% Each student is assigned to exactly one team
1 { assigned(S, T) : team(T) } 1 :- student(S).

% Team sizes: one team has 2 members, the other has 3 members
% Ensure green team has either 2 or 3 members
:- team(T), #count{S : assigned(S, T)} != 2, #count{S : assigned(S, T)} != 3.

% Ensure exactly one team has 2 members and the other has 3
:- #count{T : #count{S : assigned(S, T)} = 2} != 1.
:- #count{T : #count{S : assigned(S, T)} = 3} != 1.

% Lateefah is on green team
:- not assigned(lateefah, green).

% Each team has exactly one facilitator
{ facilitator(S) : student(S) } 1.
:- team(T), #count{S : facilitator(S), assigned(S, T)} != 1.

% Olga is a facilitator
:- not facilitator(olga).

% Kelly is not a facilitator
:- facilitator(kelly).

% Juana and Olga are on different teams
:- assigned(juana, T), assigned(olga, T).

% Lateefah is a facilitator (given condition)
:- not facilitator(lateefah).

% Map the correct answer to option/1
% Option A: Juana and Kelly are both assigned to the red team
option(a) :- assigned(juana, red), assigned(kelly, red).

% Option B: Juana and Mei are both assigned to the red team
option(b) :- assigned(juana, red), assigned(mei, red).

% Option C: Lateefah and Olga are both assigned to the green team
option(c) :- assigned(lateefah, green), assigned(olga, green).

% Option D: Mei and Olga are both assigned to the green team
option(d) :- assigned(mei, green), assigned(olga, green).

% Option E: Mei and Olga are both assigned to the red team
option(e) :- assigned(mei, red), assigned(olga, red).

#show option/1.