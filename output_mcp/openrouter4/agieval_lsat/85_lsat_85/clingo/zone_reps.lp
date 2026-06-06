% Domain
rep(kim; mahr; parra; quinn; stuckey; tiao; udall).
zone(1;2;3).

% Each rep assigned exactly one zone
{ assigned(R, Z) : zone(Z) } 1 :- rep(R).

% Constraint 1: Exactly one of Parra or Tiao in Zone 1
1 { assigned(parra, 1); assigned(tiao, 1) } 1.

% Constraint 2: Exactly one of Tiao or Udall in Zone 2
1 { assigned(tiao, 2); assigned(udall, 2) } 1.

% Constraint 3: Parra and Quinn same zone
:- assigned(parra, Z1), assigned(quinn, Z2), Z1 != Z2.

% Constraint 4: Stuckey and Udall same zone
:- assigned(stuckey, Z1), assigned(udall, Z2), Z1 != Z2.

% Constraint 5: More reps in Zone 3 than in Zone 2
count_zone2(N2) :- N2 = #count{ R : assigned(R, 2) }.
count_zone3(N3) :- N3 = #count{ R : assigned(R, 3) }.
:- count_zone2(N2), count_zone3(N3), N3 <= N2.

% Options identifiers (not the answer predicate)
opt_id(a; b; c; d; e).

% Option zone3 membership facts
opt_zone3(a, kim).    opt_zone3(a, mahr).
opt_zone3(b, kim).    opt_zone3(b, tiao).
opt_zone3(c, parra).  opt_zone3(c, quinn).
opt_zone3(d, stuckey). opt_zone3(d, tiao). opt_zone3(d, udall).
opt_zone3(e, parra).  opt_zone3(e, quinn). opt_zone3(e, stuckey). opt_zone3(e, udall).

% Choose exactly one scenario to test
1 { scenario(O) : opt_id(O) } 1.

% If scenario(O) is selected, enforce exact zone3 membership
:- scenario(O), rep(R), assigned(R, 3), not opt_zone3(O, R).
:- scenario(O), rep(R), opt_zone3(O, R), not assigned(R, 3).

% Derive the answer predicate (option/1) from the feasible scenario
option(O) :- scenario(O).

#show option/1.