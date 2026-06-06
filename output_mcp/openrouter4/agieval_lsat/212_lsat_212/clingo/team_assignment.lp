% Domains
student(juana; kelly; lateefah; mei; olga).
team(green; red).

% Each student assigned to exactly one team
1 { assigned(S, T) : team(T) } 1 :- student(S).

% One team has 2 members, the other has 3
green_count(N) :- N = #count{ S : assigned(S, green) }.
:- green_count(N), N != 2, N != 3.

% Each team has exactly one facilitator
1 { facilitator(S) : student(S), assigned(S, T) } 1 :- team(T).

% Constraint 1: Juana and Olga on different teams
:- assigned(juana, T), assigned(olga, T).

% Constraint 2: Lateefah is on green
assigned(lateefah, green).

% Constraint 3: Kelly is not a facilitator
:- facilitator(kelly).

% Constraint 4: Olga is a facilitator
facilitator(olga).

% Given condition: Mei is assigned to the green team
assigned(mei, green).

% Show the assignments and facilitators
#show assigned/2.
#show facilitator/1.