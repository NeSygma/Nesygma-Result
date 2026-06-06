% Define the days and antiques
day(1..6).
antique(harmonica; lamp; mirror; sundial; table; vase).

% Each antique is auctioned exactly once
{auctioned_on(A, D)} :- antique(A), day(D).
:- antique(A), {auctioned_on(A, D) : day(D)} != 1.
:- day(D), {auctioned_on(A, D) : antique(A)} != 1.

% Constraint 1: The sundial is not auctioned on June 1st
:- auctioned_on(sundial, 1).

% Constraint 2: If the harmonica is auctioned on an earlier date than the lamp,
% then the mirror is also auctioned on an earlier date than the lamp
:- auctioned_on(harmonica, H), auctioned_on(lamp, L), H < L, auctioned_on(mirror, M), M >= L.

% Constraint 3: The sundial is auctioned on an earlier date than the mirror and also on an earlier date than the vase
:- auctioned_on(sundial, S), auctioned_on(mirror, M), S >= M.
:- auctioned_on(sundial, S), auctioned_on(vase, V), S >= V.

% Constraint 4: The table is auctioned on an earlier date than the harmonica or on an earlier date than the vase, but not both
% Forbid table before both harmonica and vase
:- auctioned_on(table, T), auctioned_on(harmonica, H), auctioned_on(vase, V), T < H, T < V.
% Forbid table not before either harmonica or vase (i.e., table >= harmonica AND table >= vase)
:- auctioned_on(table, T), auctioned_on(harmonica, H), auctioned_on(vase, V), T >= H, T >= V.

% Define immediately_before relationship
immediately_before(X, Y) :- auctioned_on(X, D), auctioned_on(Y, D+1), day(D), D < 6.

% Define which antiques can be immediately before the vase
possible_harmonica_before_vase :- immediately_before(harmonica, vase).
possible_lamp_before_vase     :- immediately_before(lamp, vase).
possible_mirror_before_vase   :- immediately_before(mirror, vase).
possible_sundial_before_vase  :- immediately_before(sundial, vase).
possible_table_before_vase    :- immediately_before(table, vase).

% The correct answer is the one that cannot be immediately before the vase
% So we map the correct answer to the option that is NOT possible
option(a) :- not possible_harmonica_before_vase.
option(b) :- not possible_lamp_before_vase.
option(c) :- not possible_mirror_before_vase.
option(d) :- not possible_sundial_before_vase.
option(e) :- not possible_table_before_vase.

% Ensure exactly one option is selected as the answer
1 { option(a) ; option(b) ; option(c) ; option(d) ; option(e) } 1.

#show option/1.