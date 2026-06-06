% Days and antiques
day(1..6).
antique(harmonica; lamp; mirror; sundial; table; vase).

% Assign each antique to exactly one day
1 { day(A, D) : day(D) } 1 :- antique(A).

% Each day has exactly one antique
1 { day(A, D) : antique(A) } 1 :- day(D).

% Constraint 1: The sundial is not auctioned on June 1st.
:- day(sundial, 1).

% Constraint 2: If the harmonica is auctioned on an earlier date than the lamp,
% then the mirror is also auctioned on an earlier date than the lamp.
:- day(harmonica, H), day(lamp, L), H < L, day(mirror, M), M >= L.

% Constraint 3: The sundial is auctioned on an earlier date than the mirror
% and also on an earlier date than the vase.
:- day(sundial, S), day(mirror, M), S >= M.
:- day(sundial, S), day(vase, V), S >= V.

% Constraint 4: The table is auctioned on an earlier date than the harmonica
% or on an earlier date than the vase, but not both.
:- day(table, T), day(harmonica, H), day(vase, V), T < H, T < V.  % Both true - violates XOR
:- day(table, T), day(harmonica, H), day(vase, V), T >= H, T >= V. % Neither true - violates XOR

% Debugging: Show assignments for key antiques
#show day/2.

% Multiple choice options
% (A) The table is auctioned on June 2nd and the lamp is auctioned on June 3rd.
option(a) :- day(table, 2), day(lamp, 3).

% (B) The sundial is auctioned on June 2nd and the vase is auctioned on June 3rd.
option(b) :- day(sundial, 2), day(vase, 3).

% (C) The mirror is auctioned on June 3rd and the sundial is auctioned on June 4th.
option(c) :- day(mirror, 3), day(sundial, 4).

% (D) The vase is auctioned on June 4th and the sundial is auctioned on June 5th.
option(d) :- day(vase, 4), day(sundial, 5).

% (E) The sundial is auctioned on June 4th and the table is auctioned on June 5th.
option(e) :- day(sundial, 4), day(table, 5).

#show option/1.