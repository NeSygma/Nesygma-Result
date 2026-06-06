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
1 { facilitator(S) : student(S), assigned(S, T) } 1 :- team(T).

% Juana and Olga are on different teams
:- assigned(juana, T), assigned(olga, T).

% Lateefah is on green team
assigned(lateefah, green).

% Kelly is not a facilitator
:- facilitator(kelly).

% Olga is a facilitator (fact)
facilitator(olga).

% Define truth of each option
option_a_true :- facilitator(lateefah), assigned(lateefah, T), assigned(kelly, T).
option_b_true :- facilitator(mei), assigned(mei, T), assigned(kelly, T).
option_c_true :- assigned(olga, T), assigned(mei, T).
option_d_true :- facilitator(lateefah), assigned(lateefah, T1), assigned(juana, T2), T1 != T2.
option_e_true :- facilitator(mei), assigned(mei, T1), assigned(olga, T2), T1 != T2.

% Show all relevant atoms
#show assigned/2.
#show facilitator/1.
#show size/2.
#show option_a_true/0.
#show option_b_true/0.
#show option_c_true/0.
#show option_d_true/0.
#show option_e_true/0.