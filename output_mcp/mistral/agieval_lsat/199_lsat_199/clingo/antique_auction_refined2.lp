% Define the days and antiques
day(1..6).
antique(harmonica; lamp; mirror; sundial; table; vase).

% Each antique is auctioned exactly once
1 { auctioned_on(A, D) : day(D) } 1 :- antique(A).
1 { auctioned_on(A, D) : antique(A) } 1 :- day(D).

% Constraint 1: The sundial is not auctioned on June 1st
:- auctioned_on(sundial, 1).

% Constraint 2: If the harmonica is auctioned on an earlier date than the lamp,
% then the mirror is also auctioned on an earlier date than the lamp
:- auctioned_on(harmonica, H), auctioned_on(lamp, L), H < L, auctioned_on(mirror, M), M >= L.

% Constraint 3: The sundial is auctioned on an earlier date than the mirror and also on an earlier date than the vase
:- auctioned_on(sundial, S), auctioned_on(mirror, M), S >= M.
:- auctioned_on(sundial, S), auctioned_on(vase, V), S >= V.

% Constraint 4: The table is auctioned on an earlier date than the harmonica or on an earlier date than the vase, but not both
% Case 1: Table is before harmonica but not before vase
:- auctioned_on(table, T), auctioned_on(harmonica, H), auctioned_on(vase, V), T < H, T >= V.
% Case 2: Table is before vase but not before harmonica
:- auctioned_on(table, T), auctioned_on(harmonica, H), auctioned_on(vase, V), T >= H, T < V.
% Case 3: Table is before both harmonica and vase (forbidden)
:- auctioned_on(table, T), auctioned_on(harmonica, H), auctioned_on(vase, V), T < H, T < V.
% Case 4: Table is after both harmonica and vase (forbidden)
:- auctioned_on(table, T), auctioned_on(harmonica, H), auctioned_on(vase, V), T >= H, T >= V.

% Define the day of the vase
vase_day(D) :- auctioned_on(vase, D).

% Define the antique immediately before the vase
immediately_before_vase(A) :-
    auctioned_on(A, D),
    vase_day(D+1),
    day(D),
    D < 6.

% Check which antiques can be immediately before the vase
possible_harmonica_before_vase :- immediately_before_vase(harmonica).
possible_lamp_before_vase     :- immediately_before_vase(lamp).
possible_mirror_before_vase   :- immediately_before_vase(mirror).
possible_sundial_before_vase  :- immediately_before_vase(sundial).
possible_table_before_vase    :- immediately_before_vase(table).

% Identify which antiques cannot be immediately before the vase
answer_harmonica :- not possible_harmonica_before_vase.
answer_lamp     :- not possible_lamp_before_vase.
answer_mirror   :- not possible_mirror_before_vase.
answer_sundial  :- not possible_sundial_before_vase.
answer_table    :- not possible_table_before_vase.

% Map the correct answer to the option
option(a) :- answer_harmonica.
option(b) :- answer_lamp.
option(c) :- answer_mirror.
option(d) :- answer_sundial.
option(e) :- answer_table.

% Ensure exactly one option is selected as the answer
1 { option(a) ; option(b) ; option(c) ; option(d) ; option(e) } 1.

#show option/1.