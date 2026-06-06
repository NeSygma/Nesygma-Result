% Domain
rep(kim). rep(mahr). rep(parra). rep(quinn). rep(stuckey). rep(tiao). rep(udall).
zone(1). zone(2). zone(3).

% Each rep assigned to exactly one zone
1 { assigned(R, Z) : zone(Z) } 1 :- rep(R).

% Constraint 1: Either Parra or Tiao (but not both) in Zone 1
:- assigned(parra, 1), assigned(tiao, 1).
:- not assigned(parra, 1), not assigned(tiao, 1).

% Constraint 2: Either Tiao or Udall (but not both) in Zone 2
:- assigned(tiao, 2), assigned(udall, 2).
:- not assigned(tiao, 2), not assigned(udall, 2).

% Constraint 3: Parra and Quinn same zone
:- assigned(parra, Z1), assigned(quinn, Z2), Z1 != Z2.

% Constraint 4: Stuckey and Udall same zone
:- assigned(stuckey, Z1), assigned(udall, Z2), Z1 != Z2.

% Constraint 5: More reps in Zone 3 than Zone 2
count3(N) :- N = #count { R : assigned(R, 3) }.
count2(M) :- M = #count { R : assigned(R, 2) }.
:- count3(N), count2(M), N <= M.

% Additional condition: Mahr and Stuckey same zone
:- assigned(mahr, Z1), assigned(stuckey, Z2), Z1 != Z2.

% Check each option - which COULD be true (possible in at least one valid assignment)
option(a) :- assigned(kim, 2).
option(b) :- assigned(mahr, 1).
option(c) :- assigned(parra, 3).
option(d) :- assigned(stuckey, 2).
option(e) :- assigned(tiao, 1).

#show option/1.