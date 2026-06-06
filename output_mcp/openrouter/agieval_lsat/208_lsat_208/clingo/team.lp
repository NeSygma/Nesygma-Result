% Students
student(juana).
student(kelly).
student(lateefah).
student(mei).
student(olga).

% Option A facts
team_a(green, juana).
team_a(green, lateefah).
team_a(green, olga).
team_a(red, kelly).
team_a(red, mei).
fac_a(olga). % facilitator of green team
fac_a(mei).  % facilitator of red team

% Option B facts
team_b(green, kelly).
team_b(green, lateefah).
team_b(green, olga).
team_b(red, juana).
team_b(red, mei).
fac_b(lateefah).
fac_b(mei).

% Option C facts
team_c(green, kelly).
team_c(green, lateefah).
team_c(green, olga).
team_c(red, juana).
team_c(red, mei).
fac_c(olga).
fac_c(juana).

% Option D facts
team_d(green, kelly).
team_d(green, mei).
team_d(green, olga).
team_d(red, juana).
team_d(red, lateefah).
fac_d(olga).
fac_d(juana).

% Option E facts
team_e(green, lateefah).
team_e(green, olga).
team_e(red, juana).
team_e(red, kelly).
team_e(red, mei).
fac_e(olga).
fac_e(juana).

% ----- Common constraints for each option -----
% Lateefah must be on green team
bad_a :- not team_a(green, lateefah).
bad_b :- not team_b(green, lateefah).
bad_c :- not team_c(green, lateefah).
bad_d :- not team_d(green, lateefah).
bad_e :- not team_e(green, lateefah).

% Juana and Olga on different teams
bad_a :- team_a(green, juana), team_a(green, olga).
bad_a :- team_a(red, juana), team_a(red, olga).
bad_b :- team_b(green, juana), team_b(green, olga).
bad_b :- team_b(red, juana), team_b(red, olga).
bad_c :- team_c(green, juana), team_c(green, olga).
bad_c :- team_c(red, juana), team_c(red, olga).
bad_d :- team_d(green, juana), team_d(green, olga).
bad_d :- team_d(red, juana), team_d(red, olga).
bad_e :- team_e(green, juana), team_e(green, olga).
bad_e :- team_e(red, juana), team_e(red, olga).

% Kelly not a facilitator
bad_a :- fac_a(kelly).
bad_b :- fac_b(kelly).
bad_c :- fac_c(kelly).
bad_d :- fac_d(kelly).
bad_e :- fac_e(kelly).

% Olga must be a facilitator
bad_a :- not fac_a(olga).
bad_b :- not fac_b(olga).
bad_c :- not fac_c(olga).
bad_d :- not fac_d(olga).
bad_e :- not fac_e(olga).

% Team size constraints (2 and 3 members)
% Helper counts for each option
count_g_a(N) :- N = #count{S : team_a(green, S)}.
count_r_a(M) :- M = #count{S : team_a(red, S)}.
valid_a :- count_g_a(2), count_r_a(3).
valid_a :- count_g_a(3), count_r_a(2).
bad_a :- not valid_a.

count_g_b(N) :- N = #count{S : team_b(green, S)}.
count_r_b(M) :- M = #count{S : team_b(red, S)}.
valid_b :- count_g_b(2), count_r_b(3).
valid_b :- count_g_b(3), count_r_b(2).
bad_b :- not valid_b.

count_g_c(N) :- N = #count{S : team_c(green, S)}.
count_r_c(M) :- M = #count{S : team_c(red, S)}.
valid_c :- count_g_c(2), count_r_c(3).
valid_c :- count_g_c(3), count_r_c(2).
bad_c :- not valid_c.

count_g_d(N) :- N = #count{S : team_d(green, S)}.
count_r_d(M) :- M = #count{S : team_d(red, S)}.
valid_d :- count_g_d(2), count_r_d(3).
valid_d :- count_g_d(3), count_r_d(2).
bad_d :- not valid_d.

count_g_e(N) :- N = #count{S : team_e(green, S)}.
count_r_e(M) :- M = #count{S : team_e(red, S)}.
valid_e :- count_g_e(2), count_r_e(3).
valid_e :- count_g_e(3), count_r_e(2).
bad_e :- not valid_e.

% Exactly one facilitator per team
fac_g_a(N) :- N = #count{S : fac_a(S), team_a(green, S)}.
fac_r_a(M) :- M = #count{S : fac_a(S), team_a(red, S)}.
bad_a :- fac_g_a(N), N != 1.
bad_a :- fac_r_a(M), M != 1.

fac_g_b(N) :- N = #count{S : fac_b(S), team_b(green, S)}.
fac_r_b(M) :- M = #count{S : fac_b(S), team_b(red, S)}.
bad_b :- fac_g_b(N), N != 1.
bad_b :- fac_r_b(M), M != 1.

fac_g_c(N) :- N = #count{S : fac_c(S), team_c(green, S)}.
fac_r_c(M) :- M = #count{S : fac_c(S), team_c(red, S)}.
bad_c :- fac_g_c(N), N != 1.
bad_c :- fac_r_c(M), M != 1.

fac_g_d(N) :- N = #count{S : fac_d(S), team_d(green, S)}.
fac_r_d(M) :- M = #count{S : fac_d(S), team_d(red, S)}.
bad_d :- fac_g_d(N), N != 1.
bad_d :- fac_r_d(M), M != 1.

fac_g_e(N) :- N = #count{S : fac_e(S), team_e(green, S)}.
fac_r_e(M) :- M = #count{S : fac_e(S), team_e(red, S)}.
bad_e :- fac_g_e(N), N != 1.
bad_e :- fac_r_e(M), M != 1.

% Each student appears exactly once in a team
bad_a :- team_a(green, S), team_a(red, S).
bad_b :- team_b(green, S), team_b(red, S).
bad_c :- team_c(green, S), team_c(red, S).
bad_d :- team_d(green, S), team_d(red, S).
bad_e :- team_e(green, S), team_e(red, S).

% No missing student
bad_a :- student(S), not team_a(green, S), not team_a(red, S).
bad_b :- student(S), not team_b(green, S), not team_b(red, S).
bad_c :- student(S), not team_c(green, S), not team_c(red, S).
bad_d :- student(S), not team_d(green, S), not team_d(red, S).
bad_e :- student(S), not team_e(green, S), not team_e(red, S).

% Derive option if not bad
option(a) :- not bad_a.
option(b) :- not bad_b.
option(c) :- not bad_c.
option(d) :- not bad_d.
option(e) :- not bad_e.

#show option/1.