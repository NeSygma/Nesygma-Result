% Define representatives and zones
rep(kim). rep(mahr). rep(parra). rep(quinn). rep(stuckey). rep(tiao). rep(udall).
zone(zone1). zone(zone2). zone(zone3).

% Each rep works in exactly one zone
1 { works_in(R, Z) : zone(Z) } 1 :- rep(R).

% Constraint 1: Either Parra or Tiao (but not both) works in Zone 1
:- works_in(parra, zone1), works_in(tiao, zone1).
:- not 1 { works_in(parra, zone1) } 1.
:- not 1 { works_in(tiao, zone1) } 1.

% Constraint 2: Either Tiao or Udall (but not both) works in Zone 2
:- works_in(tiao, zone2), works_in(udall, zone2).
:- not 1 { works_in(tiao, zone2) } 1.
:- not 1 { works_in(udall, zone2) } 1.

% Constraint 3: Parra and Quinn work in the same zone
:- rep(parra), rep(quinn), not works_in(parra, Z), works_in(quinn, Z).

% Constraint 4: Stuckey and Udall work in the same zone
:- rep(stuckey), rep(udall), not works_in(stuckey, Z), works_in(udall, Z).

% Constraint 5: More reps in Zone 3 than Zone 2
% Count reps in each zone
count_zone(Z, N) :- N = #count { R : works_in(R, Z) }.
:- count_zone(zone3, N3), count_zone(zone2, N2), N3 =< N2.

% Given condition: Mahr and Stuckey work in the same zone
:- not 1 { Z : works_in(mahr, Z), works_in(stuckey, Z) } 1.

% Map the options to which could be true
% Option A: Kim works in Zone 2
option(a) :- works_in(kim, zone2).

% Option B: Mahr works in Zone 1
option(b) :- works_in(mahr, zone1).

% Option C: Parra works in Zone 3
option(c) :- works_in(parra, zone3).

% Option D: Stuckey works in Zone 2
option(d) :- works_in(stuckey, zone2).

% Option E: Tiao works in Zone 1
option(e) :- works_in(tiao, zone1).

#show option/1.