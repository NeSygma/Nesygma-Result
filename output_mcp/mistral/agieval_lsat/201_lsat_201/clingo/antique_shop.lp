% Days and antiques
day(1..6).
antique(harmonica; lamp; mirror; sundial; table; vase).

% Assign each antique to a unique day
1 { assigned(A, D) : day(D) } 1 :- antique(A).
1 { assigned(A, D) : antique(A) } 1 :- day(D).

% Constraint 1: Sundial is not auctioned on June 1st
:- assigned(sundial, 1).

% Helper predicate: antique A is before antique B
before(A, B) :- assigned(A, D1), assigned(B, D2), D1 < D2.

% Constraint 2: If harmonica is before lamp, then mirror is before lamp
:- before(harmonica, lamp), not before(mirror, lamp).

% Constraint 3: Sundial before mirror AND sundial before vase
:- assigned(sundial, D_s), assigned(mirror, D_m), D_s >= D_m.
:- assigned(sundial, D_s), assigned(vase, D_v), D_s >= D_v.

% Constraint 4: Table is before harmonica or before vase, but not both
% Exactly one of the two conditions holds
has_table_before_harmonica :- assigned(table, D_t), assigned(harmonica, D_h), D_t < D_h.
has_table_before_vase :- assigned(table, D_t), assigned(vase, D_v), D_t < D_v.
:- has_table_before_harmonica + has_table_before_vase != 1.

% Define the options
% Option A: Sundial on June 5th
option(a) :- assigned(sundial, 5).

% Option B: Sundial on June 4th
option(b) :- assigned(sundial, 4).

% Option C: Lamp on June 5th AND mirror on June 6th
option(c) :- assigned(lamp, 5), assigned(mirror, 6).

% Option D: Table on June 3rd AND lamp on June 4th
option(d) :- assigned(table, 3), assigned(lamp, 4).

% Option E: Harmonica on June 2nd AND vase on June 3rd
option(e) :- assigned(harmonica, 2), assigned(vase, 3).

#show option/1.