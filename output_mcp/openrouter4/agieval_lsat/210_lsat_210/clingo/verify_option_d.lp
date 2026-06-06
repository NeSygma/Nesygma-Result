% Students
student(juana; kelly; lateefah; mei; olga).

% Teams
team(green; red).

% Each student assigned to exactly one team
{ assigned(S, T) : team(T) } 1 :- student(S).

% Team sizes: one team has 2, the other has 3
size(T, N) :- N = #count{ S : assigned(S, T) }, team(T).
:- size(green, N1), size(red, N2), N1 + N2 != 5.
:- size(_, N), N < 2.
:- size(_, N), N > 3.
:- size(green, N), size(red, N).

% Each team has exactly one facilitator
1 { facilitator(S) : assigned(S, T) } 1 :- team(T).

% Juana and Olga on different teams
:- assigned(juana, T), assigned(olga, T).

% Lateefah on green team
assigned(lateefah, green).

% Kelly not facilitator
:- facilitator(kelly).

% Olga is facilitator
facilitator(olga).

% Force option D: Lateefah is a facilitator, and she is assigned to a different team than Juana is.
facilitator(lateefah).
:- assigned(lateefah, T1), assigned(juana, T2), T1 = T2.

#show assigned/2.
#show facilitator/1.