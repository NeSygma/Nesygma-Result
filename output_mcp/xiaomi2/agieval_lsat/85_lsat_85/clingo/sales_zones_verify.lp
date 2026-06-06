% Domain definitions
rep(kim). rep(mahr). rep(parra). rep(quinn). rep(stuckey). rep(tiao). rep(udall).
zone(1). zone(2). zone(3).

% Each rep is assigned to exactly one zone
1 { assign(Rep, Z) : zone(Z) } 1 :- rep(Rep).

% Constraint 1: Either Parra or Tiao (but not both) works in Zone 1
assign(parra, 1) | assign(tiao, 1).
:- assign(parra, 1), assign(tiao, 1).

% Constraint 2: Either Tiao or Udall (but not both) works in Zone 2
assign(tiao, 2) | assign(udall, 2).
:- assign(tiao, 2), assign(udall, 2).

% Constraint 3: Parra and Quinn work in the same zone
:- assign(parra, Z1), assign(quinn, Z2), Z1 != Z2.

% Constraint 4: Stuckey and Udall work in the same zone
:- assign(stuckey, Z1), assign(udall, Z2), Z1 != Z2.

% Constraint 5: More reps in Zone 3 than in Zone 2
count3(N) :- N = #count { Rep : assign(Rep, 3) }.
count2(N) :- N = #count { Rep : assign(Rep, 2) }.
:- count3(N3), count2(N2), N3 <= N2.

% Check each option: Zone 3 exactly matches the given set
% Option A: Zone 3 = {Kim, Mahr}
zone3_a :- assign(kim, 3), assign(mahr, 3),
           not assign(parra, 3), not assign(quinn, 3),
           not assign(stuckey, 3), not assign(tiao, 3), not assign(udall, 3).

% Option B: Zone 3 = {Kim, Tiao}
zone3_b :- assign(kim, 3), assign(tiao, 3),
           not assign(mahr, 3), not assign(parra, 3), not assign(quinn, 3),
           not assign(stuckey, 3), not assign(udall, 3).

% Option C: Zone 3 = {Parra, Quinn}
zone3_c :- assign(parra, 3), assign(quinn, 3),
           not assign(kim, 3), not assign(mahr, 3),
           not assign(stuckey, 3), not assign(tiao, 3), not assign(udall, 3).

% Option D: Zone 3 = {Stuckey, Tiao, Udall}
zone3_d :- assign(stuckey, 3), assign(tiao, 3), assign(udall, 3),
           not assign(kim, 3), not assign(mahr, 3),
           not assign(parra, 3), not assign(quinn, 3).

% Option E: Zone 3 = {Parra, Quinn, Stuckey, Udall}
zone3_e :- assign(parra, 3), assign(quinn, 3), assign(stuckey, 3), assign(udall, 3),
           not assign(kim, 3), not assign(mahr, 3), not assign(tiao, 3).

% Derive options
option(a) :- zone3_a.
option(b) :- zone3_b.
option(c) :- zone3_c.
option(d) :- zone3_d.
option(e) :- zone3_e.

% Show which options are possible
#show option/1.
#show zone3_a.
#show zone3_b.
#show zone3_c.
#show zone3_d.
#show zone3_e.