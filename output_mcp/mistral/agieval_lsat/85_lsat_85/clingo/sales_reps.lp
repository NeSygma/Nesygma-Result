% Define representatives and zones
rep(kim; mahr; parra; quinn; stuckey; tiao; udall).
zone(zone1; zone2; zone3).

% Each representative works in exactly one zone
1 { works_in(R, Z) : zone(Z) } 1 :- rep(R).

% Constraint 1: Either Parra or Tiao (but not both) works in Zone 1
:- works_in(parra, zone1), works_in(tiao, zone1).
:- not works_in(parra, zone1), not works_in(tiao, zone1).

% Constraint 2: Either Tiao or Udall (but not both) works in Zone 2
:- works_in(tiao, zone2), works_in(udall, zone2).
:- not works_in(tiao, zone2), not works_in(udall, zone2).

% Constraint 3: Parra and Quinn work in the same sales zone
works_in(parra, Z) :- works_in(quinn, Z), zone(Z).
works_in(quinn, Z) :- works_in(parra, Z), zone(Z).

% Constraint 4: Stuckey and Udall work in the same sales zone
works_in(stuckey, Z) :- works_in(udall, Z), zone(Z).
works_in(udall, Z) :- works_in(stuckey, Z), zone(Z).

% Helper predicates for counting representatives in zones
zone2_rep(R) :- works_in(R, zone2).
zone3_rep(R) :- works_in(R, zone3).

count_zone2(N) :- N = #count { R : zone2_rep(R) }.
count_zone3(N) :- N = #count { R : zone3_rep(R) }.

% Constraint 5: More representatives in Zone 3 than in Zone 2
:- count_zone2(N2), count_zone3(N3), N3 =< N2.

% Define the zone3 sets for each option (exact complete lists)
% Option A: Kim, Mahr in zone3 (exactly these two)
option(a) :- works_in(kim, zone3), works_in(mahr, zone3),
             count_zone3(2),
             not zone3_rep(parra), not zone3_rep(quinn),
             not zone3_rep(stuckey), not zone3_rep(tiao),
             not zone3_rep(udall).

% Option B: Kim, Tiao in zone3 (exactly these two)
option(b) :- works_in(kim, zone3), works_in(tiao, zone3),
             count_zone3(2),
             not zone3_rep(mahr), not zone3_rep(parra),
             not zone3_rep(quinn), not zone3_rep(stuckey),
             not zone3_rep(udall).

% Option C: Parra, Quinn in zone3 (exactly these two)
option(c) :- works_in(parra, zone3), works_in(quinn, zone3),
             count_zone3(2),
             not zone3_rep(kim), not zone3_rep(mahr),
             not zone3_rep(stuckey), not zone3_rep(tiao),
             not zone3_rep(udall).

% Option D: Stuckey, Tiao, Udall in zone3 (exactly these three)
option(d) :- works_in(stuckey, zone3), works_in(tiao, zone3), works_in(udall, zone3),
             count_zone3(3),
             not zone3_rep(kim), not zone3_rep(mahr),
             not zone3_rep(parra), not zone3_rep(quinn).

% Option E: Parra, Quinn, Stuckey, Udall in zone3 (exactly these four)
option(e) :- works_in(parra, zone3), works_in(quinn, zone3),
             works_in(stuckey, zone3), works_in(udall, zone3),
             count_zone3(4),
             not zone3_rep(kim), not zone3_rep(mahr),
             not zone3_rep(tiao).

#show option/1.