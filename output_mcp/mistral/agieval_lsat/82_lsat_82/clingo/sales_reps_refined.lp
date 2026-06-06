% Define representatives and zones
rep(kim). rep(mahr). rep(parra). rep(quinn). rep(stuckey). rep(tiao). rep(udall).
zone(zone1). zone(zone2). zone(zone3).

% Each rep works in exactly one zone
1 { works_in(R, Z) : zone(Z) } 1 :- rep(R).

% Constraint 1: Either Parra or Tiao (but not both) works in Zone 1
:- works_in(parra, zone1), works_in(tiao, zone1).
:- not works_in(parra, zone1), not works_in(tiao, zone1).

% Constraint 2: Either Tiao or Udall (but not both) works in Zone 2
:- works_in(tiao, zone2), works_in(udall, zone2).
:- not works_in(tiao, zone2), not works_in(udall, zone2).

% Constraint 3: Parra and Quinn work in the same zone
:- works_in(parra, Z1), works_in(quinn, Z2), Z1 != Z2.

% Constraint 4: Stuckey and Udall work in the same zone
:- works_in(stuckey, Z1), works_in(udall, Z2), Z1 != Z2.

% Constraint 5: More reps in Zone 3 than in Zone 2
% Count reps in each zone
count_zone(Z, N) :- zone(Z), N = #count { R : works_in(R, Z) }.
:- count_zone(zone3, N3), count_zone(zone2, N2), N3 <= N2.

% Define what each option means
% Option A: Zone 1: Kim, Parra; Zone 2: Stuckey, Udall; Zone 3: Mahr, Quinn, Tiao
option(a) :- works_in(kim, zone1), works_in(parra, zone1),
             works_in(stuckey, zone2), works_in(udall, zone2),
             works_in(mahr, zone3), works_in(quinn, zone3), works_in(tiao, zone3).

% Option B: Zone 1: Kim, Tiao; Zone 2: Stuckey, Udall; Zone 3: Mahr, Parra, Quinn
option(b) :- works_in(kim, zone1), works_in(tiao, zone1),
             works_in(stuckey, zone2), works_in(udall, zone2),
             works_in(mahr, zone3), works_in(parra, zone3), works_in(quinn, zone3).

% Option C: Zone 1: Parra, Quinn; Zone 2: Kim, Udall; Zone 3: Mahr, Stuckey, Tiao
option(c) :- works_in(parra, zone1), works_in(quinn, zone1),
             works_in(kim, zone2), works_in(udall, zone2),
             works_in(mahr, zone3), works_in(stuckey, zone3), works_in(tiao, zone3).

% Option D: Zone 1: Stuckey, Udall; Zone 2: Kim, Tiao; Zone 3: Mahr, Parra, Quinn
option(d) :- works_in(stuckey, zone1), works_in(udall, zone1),
             works_in(kim, zone2), works_in(tiao, zone2),
             works_in(mahr, zone3), works_in(parra, zone3), works_in(quinn, zone3).

% Option E: Zone 1: Tiao; Zone 2: Kim, Parra, Quinn; Zone 3: Stuckey, Udall
option(e) :- works_in(tiao, zone1),
             works_in(kim, zone2), works_in(parra, zone2), works_in(quinn, zone2),
             works_in(stuckey, zone3), works_in(udall, zone3).

% Ensure only one option is selected
:- option(X), option(Y), X != Y.

% Show the option
#show option/1.