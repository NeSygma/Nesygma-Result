% Representatives
rep(kim). rep(mahr). rep(parra). rep(quinn). rep(stuckey). rep(tiao). rep(udall).

% Zones
zone(1). zone(2). zone(3).

% Each representative is assigned to exactly one zone
1 { assign(R, Z) : zone(Z) } 1 :- rep(R).

% Constraint 1: Exactly one of Parra and Tiao in Zone 1
1 { assign(parra,1); assign(tiao,1) } 1.

% Constraint 2: Exactly one of Tiao and Udall in Zone 2
1 { assign(tiao,2); assign(udall,2) } 1.

% Constraint 3: Parra and Quinn in the same zone
:- assign(parra, Z1), assign(quinn, Z2), Z1 != Z2.

% Constraint 4: Stuckey and Udall in the same zone
:- assign(stuckey, Z1), assign(udall, Z2), Z1 != Z2.

% Constraint 5: More representatives in Zone 3 than in Zone 2
count2(N2) :- N2 = #count { R : assign(R,2) }.
count3(N3) :- N3 = #count { R : assign(R,3) }.
:- count2(N2), count3(N3), N3 <= N2.

% Define together_possible for each option
together_possible(kim) :- assign(quinn,Z), assign(kim,Z).
together_possible(mahr) :- assign(quinn,Z), assign(mahr,Z).
together_possible(stuckey) :- assign(quinn,Z), assign(stuckey,Z).
together_possible(tiao) :- assign(quinn,Z), assign(tiao,Z).
together_possible(udall) :- assign(quinn,Z), assign(udall,Z).

% Define answer for each option: true if together_possible is false in this model
answer(a) :- not together_possible(kim).
answer(b) :- not together_possible(mahr).
answer(c) :- not together_possible(stuckey).
answer(d) :- not together_possible(tiao).
answer(e) :- not together_possible(udall).

#show answer/1.