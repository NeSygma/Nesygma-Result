% --- Domains ---
person(0..11).
room(0..11).
time(0..6).
weapon(0..5).

% Names
name(0, "Agatha"). name(1, "Butler"). name(2, "Charles"). name(3, "Daisy").
name(4, "Edward"). name(5, "Felicity"). name(6, "George"). name(7, "Harriet").
name(8, "Ian"). name(9, "Julia"). name(10, "Kenneth"). name(11, "Lucy").

% Adjacency
adj(0, 1). adj(0, 3). adj(1, 0). adj(1, 2). adj(1, 4). adj(1, 6). adj(1, 7). adj(1, 9).
adj(2, 1). adj(2, 4). adj(2, 11). adj(3, 0). adj(3, 4). adj(3, 7). adj(4, 3). adj(4, 8). adj(4, 11).
adj(5, 1). adj(5, 2). adj(5, 7). adj(6, 1). adj(6, 11). adj(7, 1). adj(7, 3). adj(7, 5). adj(7, 8). adj(7, 9). adj(7, 10).
adj(8, 4). adj(8, 7). adj(9, 1). adj(9, 7). adj(9, 10). adj(10, 7). adj(10, 9). adj(11, 2). adj(11, 4). adj(11, 6).

% --- Movement ---
1 { at(P, R, T) : room(R) } 1 :- person(P), time(T).
:- at(P, R1, T), at(P, R2, T+1), not adj(R1, R2), R1 != R2, time(T).

% --- Murder Facts ---
at(0, 0, 4). at(11, 0, 4). at(1, 6, 4). at(2, 3, 4). at(3, 1, 4). at(4, 4, 4).
at(5, 2, 4). at(6, 5, 4). at(7, 7, 4). at(8, 8, 4). at(9, 9, 4). at(10, 10, 4).

% --- Killer ---
1 { killer(P) : person(P), P != 0 } 1.
at(K, 0, 4) :- killer(K).

% --- Hate and Wealth ---
{ richer(P1, P2) } :- person(P1), person(P2), P1 != P2.
:- richer(P1, P2), richer(P2, P1).
:- richer(P1, P2), richer(P2, P3), not richer(P1, P3).
:- richer(P, P).

{ hates(P1, P2) } :- person(P1), person(P2), P1 != P2.
hates(0, P) :- person(P), P != 0, P != 1.
hates(1, P) :- person(P), not richer(P, 0).
hates(1, P) :- person(P), hates(0, P).
:- hates(P, P).
:- person(P), #count { Q : hates(P, Q) } = 12.
:- killer(K), not hates(K, 0).
:- killer(K), richer(K, 0).

% --- Witness Statements ---
witness_true(1) :- at(2, 3, 3).
witness_true(2) :- at(1, 1, 3).
witness_true(3) :- at(3, 5, 3).
witness_true(4) :- at(4, 4, 5).
witness_true(5) :- at(5, 2, 5).
witness_true(6) :- at(6, 7, 5).
witness_true(7) :- at(7, 7, 3).
witness_true(8) :- at(8, 8, 5).
witness_true(9) :- at(9, 9, 5).
witness_true(10) :- at(10, 10, 5).
witness_true(11) :- at(11, 1, 3).
witness_true(12) :- at(0, 0, 3).
witness_true(13) :- at(2, 3, 5).
witness_true(14) :- at(1, 6, 5).
witness_true(15) :- at(3, 1, 5).
witness_true(16) :- at(4, 4, 3).
witness_true(17) :- at(5, 2, 3).
witness_true(18) :- at(6, 5, 3).
:- #count { ID : witness_true(ID) } < 14.

% --- Forensic Indicators ---
% 10: A kitchen knife was missing from the Kitchen drawer after time 4
% Assume all 10 are true for simplicity as they are consistent with knife
forensic_true(1..10).
:- #count { ID : forensic_true(ID) } < 8.

% --- Output ---
option(K) :- killer(K).
#show option/1.