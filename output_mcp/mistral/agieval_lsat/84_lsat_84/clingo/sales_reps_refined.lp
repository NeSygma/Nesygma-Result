% Define the representatives and zones
rep(kim; mahr; parra; quinn; stuckey; tiao; udall).
zone(1; 2; 3).

% Each representative works in exactly one zone
1 { works_in(R, Z) : zone(Z) } 1 :- rep(R).

% Either Parra or Tiao (but not both) works in Zone 1
:- 2 { works_in(parra, 1) ; works_in(tiao, 1) }.
:- not 1 { works_in(parra, 1) ; works_in(tiao, 1) }.

% Either Tiao or Udall (but not both) works in Zone 2
:- 2 { works_in(tiao, 2) ; works_in(udall, 2) }.
:- not 1 { works_in(tiao, 2) ; works_in(udall, 2) }.

% Parra and Quinn work in the same zone
:- works_in(parra, Z), works_in(quinn, Z2), Z != Z2.
works_in(parra, Z) :- works_in(quinn, Z), zone(Z).
works_in(quinn, Z) :- works_in(parra, Z), zone(Z).

% Stuckey and Udall work in the same zone
:- works_in(stuckey, Z), works_in(udall, Z2), Z != Z2.
works_in(stuckey, Z) :- works_in(udall, Z), zone(Z).
works_in(udall, Z) :- works_in(stuckey, Z), zone(Z).

% More representatives in Zone 3 than Zone 2
count_zone(Z, N) :- N = #count { R : works_in(R, Z) }, zone(Z).
:- count_zone(3, N3), count_zone(2, N2), N3 <= N2.

% Define which options are possible
possible_a :- works_in(kim, 1), works_in(stuckey, 1).
possible_b :- works_in(kim, 3), works_in(stuckey, 3).
possible_c :- works_in(mahr, 3), works_in(stuckey, 3).
possible_d :- works_in(mahr, 3), works_in(udall, 3).
possible_e :- works_in(parra, 1), works_in(stuckey, 1).

% The answer is the option that must be false (i.e., the option that is impossible)
% Only one option can be impossible
answer_a :- not possible_a, possible_b, possible_c, possible_d, possible_e.
answer_b :- not possible_b, possible_a, possible_c, possible_d, possible_e.
answer_c :- not possible_c, possible_a, possible_b, possible_d, possible_e.
answer_d :- not possible_d, possible_a, possible_b, possible_c, possible_e.
answer_e :- not possible_e, possible_a, possible_b, possible_c, possible_d.

% Map to option/1
option(a) :- answer_a.
option(b) :- answer_b.
option(c) :- answer_c.
option(d) :- answer_d.
option(e) :- answer_e.

#show option/1.