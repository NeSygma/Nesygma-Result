%% Domain
rep(kim; mahr; parra; quinn; stuckey; tiao; udall).
zone(1; 2; 3).

%% Each rep works in exactly one zone
{ assigned(R, Z) : zone(Z) } 1 :- rep(R).

%% Condition 1: Either Parra or Tiao (but not both) works in Zone 1
1 { assigned(parra, 1); assigned(tiao, 1) } 1.

%% Condition 2: Either Tiao or Udall (but not both) works in Zone 2
1 { assigned(tiao, 2); assigned(udall, 2) } 1.

%% Condition 3: Parra and Quinn work in the same zone
same_zone(R1, R2, Z) :- assigned(R1, Z), assigned(R2, Z).
:- assigned(parra, Z1), assigned(quinn, Z2), Z1 != Z2.

%% Condition 4: Stuckey and Udall work in the same zone
:- assigned(stuckey, Z1), assigned(udall, Z2), Z1 != Z2.

%% Condition 5: More reps in Zone 3 than in Zone 2
zone2_count(N2) :- N2 = #count { R : assigned(R, 2) }.
zone3_count(N3) :- N3 = #count { R : assigned(R, 3) }.
:- zone2_count(N2), zone3_count(N3), N3 <= N2.

%% Evaluate each option: check if the scenario can be true
scenario_a :- assigned(kim, 1), assigned(stuckey, 1).
scenario_b :- assigned(kim, 3), assigned(stuckey, 3).
scenario_c :- assigned(mahr, 3), assigned(stuckey, 3).
scenario_d :- assigned(mahr, 3), assigned(udall, 3).
scenario_e :- assigned(parra, 1), assigned(stuckey, 1).

%% We want to know which scenario is impossible
%% So we derive option(x) if the scenario is impossible (must be false)
option(a) :- not scenario_a.
option(b) :- not scenario_b.
option(c) :- not scenario_c.
option(d) :- not scenario_d.
option(e) :- not scenario_e.

#show option/1.
#show assigned/2.