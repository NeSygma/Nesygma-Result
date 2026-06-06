% Days and antiques
day(1..6).
antique(harmonica; lamp; mirror; sundial; table; vase).

% Each day has exactly one antique
1 { auctioned(D, A) : antique(A) } 1 :- day(D).

% Each antique is auctioned exactly once
:- antique(A), not 1 { auctioned(D, A) : day(D) } 1.

% Constraint 1: sundial is not auctioned on June 1st (day 1)
:- auctioned(1, sundial).

% Constraint 2: If harmonica is auctioned on an earlier date than the lamp, 
% then the mirror is also auctioned on an earlier date than the lamp.
% Contrapositive: If mirror is NOT before lamp (mirror >= lamp), 
% then harmonica is NOT before lamp (harmonica >= lamp)
:- auctioned(M_day, mirror), auctioned(L_day, lamp), M_day >= L_day, 
   auctioned(H_day, harmonica), H_day < L_day.

% Constraint 3: The sundial is auctioned on an earlier date than the mirror 
% and also on an earlier date than the vase.
:- auctioned(S_day, sundial), auctioned(M_day, mirror), S_day >= M_day.
:- auctioned(S_day, sundial), auctioned(V_day, vase), S_day >= V_day.

% Constraint 4: The table is auctioned on an earlier date than the harmonica 
% or on an earlier date than the vase, but not both.
% Helper predicates to count the number of conditions that are true
before_harmonica(T_day) :- auctioned(T_day, table), auctioned(H_day, harmonica), T_day < H_day.
before_vase(T_day) :- auctioned(T_day, table), auctioned(V_day, vase), T_day < V_day.

% Exactly one of the two conditions must be true
:- auctioned(T_day, table), #count { X : before_harmonica(X) ; Y : before_vase(Y) } != 1.

% Define answer(X) for each option
answer(a) :- auctioned(2, mirror).
answer(b) :- auctioned(2, lamp).
answer(c) :- auctioned(2, vase).
answer(d) :- auctioned(3, lamp).
answer(e) :- auctioned(5, mirror).

% Map the correct answer to option/1
option(X) :- answer(X).

#show option/1.