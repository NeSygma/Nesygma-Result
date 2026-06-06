% Domain
student(juana). student(kelly). student(lateefah). student(mei). student(olga).
team(green). team(red).

% Each student assigned to exactly one team
1 { assigned(S, T) : team(T) } 1 :- student(S).

% Count members on each team
green_count(N) :- N = #count { S : assigned(S, green) }.
red_count(N) :- N = #count { S : assigned(S, red) }.

% One team has 2 members, the other has 3
:- green_count(N1), red_count(N2), N1 != 2, N1 != 3.
:- green_count(N1), red_count(N2), N1 + N2 != 5.

% Each team has exactly one facilitator who is a member of that team
1 { facilitator(S) : assigned(S, T) } 1 :- team(T).

% Conditions from problem
% 1. Juana is on a different team than Olga
:- assigned(juana, T), assigned(olga, T).

% 2. Lateefah is on the green team
assigned(lateefah, green).

% 3. Kelly is not a facilitator
:- facilitator(kelly).

% 4. Olga is a facilitator
facilitator(olga).

% 5. Lateefah is a facilitator (added condition from question)
facilitator(lateefah).

% Check each option - could it be true in some valid assignment?

% Option A: Juana and Kelly both on red team
check_a :- assigned(juana, red), assigned(kelly, red).

% Option B: Juana and Mei both on red team
check_b :- assigned(juana, red), assigned(mei, red).

% Option C: Lateefah and Olga both on green team
check_c :- assigned(lateefah, green), assigned(olga, green).

% Option D: Mei and Olga both on green team
check_d :- assigned(mei, green), assigned(olga, green).

% Option E: Mei and Olga both on red team
check_e :- assigned(mei, red), assigned(olga, red).

% An option "could be true" if there exists a valid model where it holds
option(a) :- check_a.
option(b) :- check_b.
option(c) :- check_c.
option(d) :- check_d.
option(e) :- check_e.

#show option/1.
#show assigned/2.
#show facilitator/1.