% Days and antiques
day(1..6).
antique(harmonica). antique(lamp). antique(mirror). antique(sundial). antique(table). antique(vase).

% Each antique is auctioned exactly once
1 { auctioned(A, D) : day(D) } 1 :- antique(A).

% Each day has exactly one antique
1 { auctioned(A, D) : antique(A) } 1 :- day(D).

% Constraint 1: Sundial is not auctioned on June 1st
:- auctioned(sundial, 1).

% Constraint 2: If harmonica < lamp then mirror < lamp
% We need to define "earlier date" meaning smaller day number
earlier(A, B) :- auctioned(A, D1), auctioned(B, D2), D1 < D2.
:- earlier(harmonica, lamp), not earlier(mirror, lamp).

% Constraint 3: sundial < mirror AND sundial < vase
:- not earlier(sundial, mirror).
:- not earlier(sundial, vase).

% Constraint 4: table < harmonica XOR table < vase
% Exactly one of these must be true
table_before_harmonica :- earlier(table, harmonica).
table_before_vase :- earlier(table, vase).
:- table_before_harmonica, table_before_vase.  % Can't be both
:- not table_before_harmonica, not table_before_vase.  % Must be at least one

% Map the correct answer to option/1
% We need to check each option against the constraints
% Option A: harmonica, table, sundial, lamp, vase, mirror
option(a) :- auctioned(harmonica,1), auctioned(table,2), auctioned(sundial,3), auctioned(lamp,4), auctioned(vase,5), auctioned(mirror,6).

% Option B: lamp, harmonica, sundial, mirror, vase, table
option(b) :- auctioned(lamp,1), auctioned(harmonica,2), auctioned(sundial,3), auctioned(mirror,4), auctioned(vase,5), auctioned(table,6).

% Option C: harmonica, sundial, table, mirror, lamp, vase
option(c) :- auctioned(harmonica,1), auctioned(sundial,2), auctioned(table,3), auctioned(mirror,4), auctioned(lamp,5), auctioned(vase,6).

% Option D: sundial, mirror, harmonica, table, vase, lamp
option(d) :- auctioned(sundial,1), auctioned(mirror,2), auctioned(harmonica,3), auctioned(table,4), auctioned(vase,5), auctioned(lamp,6).

% Option E: vase, sundial, lamp, harmonica, table, mirror
option(e) :- auctioned(vase,1), auctioned(sundial,2), auctioned(lamp,3), auctioned(harmonica,4), auctioned(table,5), auctioned(mirror,6).

#show option/1.