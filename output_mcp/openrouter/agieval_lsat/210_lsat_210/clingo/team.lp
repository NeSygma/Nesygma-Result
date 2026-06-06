% -------------------------------------------------
% Entities
student(juana).   student(kelly).   student(lateefah).
student(mei).     student(olga).

team(green). team(red).

% -------------------------------------------------
% Assignment: each student is on exactly one team
1 { assigned(S, green); assigned(S, red) } 1 :- student(S).

% Lateefah is on the green team
assigned(lateefah, green).

% Exactly one facilitator per team
1 { facilitator(S) : assigned(S, green) } 1.
1 { facilitator(S) : assigned(S, red)   } 1.

% Given facts
facilitator(olga).          % Olga is a facilitator
:- facilitator(kelly).      % Kelly is not a facilitator
% Juana must be on a different team than Olga
:- assigned(juana, T), assigned(olga, T).

% Team size: one team has 2 members, the other 3 members
:- #count{ S : assigned(S, green) } < 2.
:- #count{ S : assigned(S, green) } > 3.
:- #count{ S : assigned(S, red)   } < 2.
:- #count{ S : assigned(S, red)   } > 3.

% -------------------------------------------------
% Helper predicates for team relations
same_team(X,Y) :- assigned(X,T), assigned(Y,T).
% different team means not same team (but both assigned)
different_team(X,Y) :- assigned(X,T1), assigned(Y,T2), T1 != T2.

% -------------------------------------------------
% Choose which option to test (exactly one)
1 { test_option(a); test_option(b); test_option(c); test_option(d); test_option(e) } 1.

% -------------------------------------------------
% Option A condition: Lateefah facilitator and same team as Kelly
:- test_option(a), not facilitator(lateefah).
:- test_option(a), not same_team(lateefah, kelly).

% Option B condition: Mei facilitator and same team as Kelly
:- test_option(b), not facilitator(mei).
:- test_option(b), not same_team(mei, kelly).

% Option C condition: Olga facilitator (already true) and same team as Mei
:- test_option(c), not same_team(olga, mei).

% Option D condition: Lateefah facilitator and different team than Juana
:- test_option(d), not facilitator(lateefah).
:- test_option(d), not different_team(lateefah, juana).

% Option E condition: Mei facilitator and different team than Olga
:- test_option(e), not facilitator(mei).
:- test_option(e), not different_team(mei, olga).

% -------------------------------------------------
% Mapping to answer options (only the must‑be‑false option is derived)
option(a) :- 0=1.
option(b) :- 0=1.
option(c) :- 0=1.
option(d) :- not test_option(d).   % D cannot be selected, therefore it is the false one
option(e) :- 0=1.

#show option/1.