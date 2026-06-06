% Define representatives
representative(kim). representative(mahr). representative(parra).
representative(quinn). representative(stuckey). representative(tiao).
representative(udall).

% Define zones
zone(zone1). zone(zone2). zone(zone3).

% Assignment: each rep works in exactly one zone
1 { assigned(R, Z) : zone(Z) } 1 :- representative(R).

% Either Parra or Tiao (but not both) works in Zone 1
1 { assigned(parra, zone1) ; assigned(tiao, zone1) } 1.

% Either Tiao or Udall (but not both) works in Zone 2
1 { assigned(tiao, zone2) ; assigned(udall, zone2) } 1.

% Parra and Quinn work in the same sales zone
:- assigned(parra, Z1), assigned(quinn, Z2), Z1 != Z2.

% Stuckey and Udall work in the same sales zone
:- assigned(stuckey, Z1), assigned(udall, Z2), Z1 != Z2.

% Count representatives in each zone
count_zone(Z, N) :- N = #count { R : assigned(R, Z) }, zone(Z).

% More in Zone 3 than Zone 2
:- count_zone(zone3, N3), count_zone(zone2, N2), N3 =< N2.

% Condition: more in Zone 1 than Zone 3
:- count_zone(zone1, N1), count_zone(zone3, N3), N1 =< N3.

% Define the options
% (A) Kim works in Zone 2
could_be_a :- assigned(kim, zone2).

% (B) Mahr works in Zone 2
could_be_b :- assigned(mahr, zone2).

% (C) Parra works in Zone 3
could_be_c :- assigned(parra, zone3).

% (D) Tiao works in Zone 1
could_be_d :- assigned(tiao, zone1).

% (E) Udall works in Zone 3
could_be_e :- assigned(udall, zone3).

% Map to option/1
option(a) :- could_be_a.
option(b) :- could_be_b.
option(c) :- could_be_c.
option(d) :- could_be_d.
option(e) :- could_be_e.

#show option/1.