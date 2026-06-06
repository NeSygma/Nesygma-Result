% Base facts: sales representatives and zones
representative(kim).
representative(mahr).
representative(parra).
representative(quinn).
representative(stuckey).
representative(tiao).
representative(udall).

zone(1..3).

% Each representative works in exactly one zone
1 { works_in(R, Z) : zone(Z) } 1 :- representative(R).

% Condition 1: Either Parra or Tiao (but not both) works in Zone 1
:- works_in(parra, 1), works_in(tiao, 1).
:- not 1 { works_in(parra, 1); works_in(tiao, 1) } 1.

% Condition 2: Either Tiao or Udall (but not both) works in Zone 2
:- works_in(tiao, 2), works_in(udall, 2).
:- not 1 { works_in(tiao, 2); works_in(udall, 2) } 1.

% Condition 3: Parra and Quinn work in the same sales zone
:- works_in(parra, Z1), works_in(quinn, Z2), Z1 != Z2.

% Condition 4: Stuckey and Udall work in the same sales zone
:- works_in(stuckey, Z1), works_in(udall, Z2), Z1 != Z2.

% Condition 5: More representatives in Zone 3 than in Zone 2
zone3_count(N) :- N = #count { R : works_in(R, 3) }.
zone2_count(N) :- N = #count { R : works_in(R, 2) }.
:- zone3_count(N3), zone2_count(N2), N3 <= N2.

% Define the options as conditions
% (A) Kim and Stuckey both work in Zone 1
option(a) :- works_in(kim, 1), works_in(stuckey, 1).

% (B) Kim and Stuckey both work in Zone 3
option(b) :- works_in(kim, 3), works_in(stuckey, 3).

% (C) Mahr and Stuckey both work in Zone 3
option(c) :- works_in(mahr, 3), works_in(stuckey, 3).

% (D) Mahr and Udall both work in Zone 3
option(d) :- works_in(mahr, 3), works_in(udall, 3).

% (E) Parra and Stuckey both work in Zone 1
option(e) :- works_in(parra, 1), works_in(stuckey, 1).

#show option/1.