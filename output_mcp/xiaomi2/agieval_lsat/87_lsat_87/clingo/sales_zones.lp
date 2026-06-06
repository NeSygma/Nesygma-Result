% Domain: sales representatives
rep(kim). rep(mahr). rep(parra). rep(quinn). rep(stuckey). rep(tiao). rep(uall).

% Domain: zones
zone(1). zone(2). zone(3).

% Each rep works in exactly one zone
1 { assigned(R, Z) : zone(Z) } 1 :- rep(R).

% Constraint 1: Either Parra or Tiao (but not both) works in Zone 1
in_zone1_parra :- assigned(parra, 1).
in_zone1_tiao :- assigned(tiao, 1).
:- in_zone1_parra, in_zone1_tiao.
:- not in_zone1_parra, not in_zone1_tiao.

% Constraint 2: Either Tiao or Udall (but not both) works in Zone 2
in_zone2_tiao :- assigned(tiao, 2).
in_zone2_uall :- assigned(uall, 2).
:- in_zone2_tiao, in_zone2_uall.
:- not in_zone2_tiao, not in_zone2_uall.

% Constraint 3: Parra and Quinn work in the same zone
:- assigned(parra, Z1), assigned(quinn, Z2), Z1 != Z2.

% Constraint 4: Stuckey and Udall work in the same zone
:- assigned(stuckey, Z1), assigned(uall, Z2), Z1 != Z2.

% Constraint 5: More reps in Zone 3 than in Zone 2
count_zone2(N2) :- N2 = #count{R : assigned(R, 2)}.
count_zone3(N3) :- N3 = #count{R : assigned(R, 3)}.
:- count_zone2(N2), count_zone3(N3), N3 <= N2.

% Additional condition: Mahr and Stuckey work in the same zone
:- assigned(mahr, Z1), assigned(stuckey, Z2), Z1 != Z2.

% Map the correct answer to option/1
option(a) :- assigned(kim, 2).
option(b) :- assigned(mahr, 1).
option(c) :- assigned(parra, 3).
option(d) :- assigned(stuckey, 2).
option(e) :- assigned(tiao, 1).

#show option/1.