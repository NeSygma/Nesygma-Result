% Base facts: sales representatives and zones
representative(kim).
representative(mahr).
representative(parra).
representative(quinn).
representative(stuckey).
representative(tiao).
representative(udall).

zone(zone1).
zone(zone2).
zone(zone3).

% Each representative works in exactly one zone
1 { works_in(R, Z) : zone(Z) } 1 :- representative(R).

% Condition 1: Either Parra or Tiao (but not both) works in Zone 1
:- works_in(parra, zone1), works_in(tiao, zone1).
:- not 1 { works_in(parra, zone1); works_in(tiao, zone1) } 1.

% Condition 2: Either Tiao or Udall (but not both) works in Zone 2
:- works_in(tiao, zone2), works_in(udall, zone2).
:- not 1 { works_in(tiao, zone2); works_in(udall, zone2) } 1.

% Condition 3: Parra and Quinn work in the same sales zone
same_zone(P, Q) :- works_in(P, Z), works_in(Q, Z), representative(P), representative(Q).
:- representative(parra), representative(quinn), not same_zone(parra, quinn).

% Condition 4: Stuckey and Udall work in the same sales zone
same_zone(S, U) :- works_in(S, Z), works_in(U, Z), representative(S), representative(U).
:- representative(stuckey), representative(udall), not same_zone(stuckey, udall).

% Condition 5: More representatives in Zone 3 than in Zone 2
% Count representatives in Zone 2 and Zone 3
count_zone2(N) :- N = #count { R : works_in(R, zone2) }.
count_zone3(M) :- M = #count { R : works_in(R, M) }.
:- count_zone2(N), count_zone3(M), M =< N.

% Additional constraint: Mahr and Stuckey work in the same sales zone
:- works_in(mahr, Z1), works_in(stuckey, Z2), Z1 != Z2.

% Map the correct answer to option/1 (MANDATORY)
% (A) Kim works in Zone 2
option(a) :- works_in(kim, zone2).

% (B) Mahr works in Zone 1
option(b) :- works_in(mahr, zone1).

% (C) Parra works in Zone 3
option(c) :- works_in(parra, zone3).

% (D) Stuckey works in Zone 2
option(d) :- works_in(stuckey, zone2).

% (E) Tiao works in Zone 1
option(e) :- works_in(tiao, zone1).

#show option/1.