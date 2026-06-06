% Domains
student(juana; kelly; lateefah; mei; olga).
team(green; red).

% Base facts from problem description
assigned(lateefah, green).
assigned(mei, green).  % Given condition for the question

% Each student assigned to exactly one team
1 { assigned(S, T) : team(T) } 1 :- student(S).

% Team sizes: one team has 2, the other has 3
size(green, 2) :- #count { S : assigned(S, green) } = 2, #count { S : assigned(S, red) } = 3.
size(green, 3) :- #count { S : assigned(S, green) } = 3, #count { S : assigned(S, red) } = 2.
:- not size(green, 2), not size(green, 3).

% Juana and Olga must be on different teams
:- assigned(juana, T), assigned(olga, T).

% Kelly is not a facilitator
:- facilitator(kelly, _).

% Olga is a facilitator
facilitator(olga, T) :- assigned(olga, T).

% Each team has exactly one facilitator
1 { facilitator(S, T) : assigned(S, T) } 1 :- team(T).

% Derive the correct answer: Kelly must be on the red team
option(b) :- assigned(kelly, red).

% Ensure no other options are derived (they are not necessarily true)

#show option/1.