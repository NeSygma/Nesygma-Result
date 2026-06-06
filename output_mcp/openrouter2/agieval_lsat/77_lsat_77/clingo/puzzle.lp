% Define businesses and spaces
business(optometrist). business(pharmacy). business(restaurant1). business(restaurant2). business(shoe). business(toy). business(veterinarian).
space(1). space(2). space(3). space(4). space(5). space(6). space(7).

% Each business occupies exactly one space
1 { pos(B,S) : space(S) } 1 :- business(B).
% Each space contains exactly one business
1 { pos(B,S) : business(B) } 1 :- space(S).

% Shoe store is in space 2
pos(shoe,2).

% Pharmacy must be at one end
1 { pos(pharmacy,1); pos(pharmacy,7) } 1.

% One restaurant at the opposite end of the pharmacy
:- pos(pharmacy,1), not pos(restaurant1,7), not pos(restaurant2,7).
:- pos(pharmacy,7), not pos(restaurant1,1), not pos(restaurant2,1).

% Restaurants must be separated by at least two other businesses
:- pos(restaurant1,S1), pos(restaurant2,S2), S1 < S2, S2 - S1 < 3.
:- pos(restaurant1,S1), pos(restaurant2,S2), S2 < S1, S1 - S2 < 3.

% Pharmacy must be next to either optometrist or veterinarian
:- pos(pharmacy,1), not pos(optometrist,2), not pos(veterinarian,2).
:- pos(pharmacy,7), not pos(optometrist,6), not pos(veterinarian,6).

% Toy store cannot be next to veterinarian
:- pos(toy,S), pos(veterinarian,V), S = V+1.
:- pos(toy,S), pos(veterinarian,V), V = S+1.

% Map options
option(a) :- pos(optometrist,5).
option(b) :- pos(pharmacy,1).
option(c) :- pos(restaurant1,3); pos(restaurant2,3).
option(d) :- pos(toy,6).
option(e) :- pos(veterinarian,4).

% Exactly one option must hold
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.