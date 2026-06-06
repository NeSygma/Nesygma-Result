% Persons
person(kim). person(mahr). person(parra). person(quinn). person(stuckey). person(tiao). person(udall).

% Zones are 1,2,3
zone_id(1..3).

% Each person assigned exactly one zone
1 { zone(P,1); zone(P,2); zone(P,3) } 1 :- person(P).

% Constraint: exactly one of Parra or Tiao in Zone1
1 { zone(parra,1); zone(tiao,1) } 1.

% Constraint: exactly one of Tiao or Udall in Zone2
1 { zone(tiao,2); zone(udall,2) } 1.

% Parra and Quinn same zone
:- zone(parra,Z1), zone(quinn,Z2), Z1 != Z2.

% Stuckey and Udall same zone
:- zone(stuckey,Z1), zone(udall,Z2), Z1 != Z2.

% More reps in Zone3 than Zone2
cnt2(N) :- N = #count { P : zone(P,2) }.
cnt3(M) :- M = #count { P : zone(P,3) }.
:- cnt2(N), cnt3(M), M <= N.

% Premise: Mahr and Stuckey work in same zone
:- zone(mahr,Z1), zone(stuckey,Z2), Z1 != Z2.

% Options choice
1 { choose(a); choose(b); choose(c); choose(d); choose(e) } 1.

% Link options to conditions
:- choose(a), not zone(kim,2).
:- choose(b), not zone(mahr,1).
:- choose(c), not zone(parra,3).
:- choose(d), not zone(stuckey,2).
:- choose(e), not zone(tiao,1).

% Map to option/1
option(a) :- choose(a).
option(b) :- choose(b).
option(c) :- choose(c).
option(d) :- choose(d).
option(e) :- choose(e).

#show option/1.