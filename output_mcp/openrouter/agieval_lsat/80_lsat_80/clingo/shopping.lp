% Spaces
space(1..7).

% Businesses (identifiers)
business(opt).
business(pharm).
business(rest1).
business(rest2).
business(shoe).
business(toy).
business(vet).

% Exactly one space per business
1 { pos(B,S) : space(S) } 1 :- business(B).
% At most one business per space
:- pos(B1,S), pos(B2,S), B1 != B2.

% Shoe store fixed at space 4
pos(shoe,4).

% Pharmacy must be at an end (space 1 or 7)
:- not pos(pharm,1), not pos(pharm,7).
% A restaurant must be at the opposite end
:- pos(pharm,1), not pos(rest1,7), not pos(rest2,7).
:- pos(pharm,7), not pos(rest1,1), not pos(rest2,1).

% Restaurants must be separated by at least two other businesses (distance >=3)
:- pos(rest1,S), pos(rest2,S+1).
:- pos(rest1,S), pos(rest2,S+2).
:- pos(rest1,S), pos(rest2,S-1).
:- pos(rest1,S), pos(rest2,S-2).

% Define adjacency between consecutive spaces
adjacent(X,Y) :- space(X), space(Y), X = Y+1.
adjacent(X,Y) :- space(X), space(Y), X+1 = Y.

% Helper predicates for pharmacy adjacency
adjacent_to_opt(P) :- adjacent(P,O), pos(opt,O).
adjacent_to_vet(P) :- adjacent(P,V), pos(vet,V).
% Pharmacy must be next to optometrist or veterinarian
:- pos(pharm,P), not adjacent_to_opt(P), not adjacent_to_vet(P).

% Toy store cannot be next to veterinarian
:- pos(toy,T), pos(vet,V), adjacent(T,V).

% Helper predicates for restaurants and adjacency
rest(R) :- pos(rest1,R).
rest(R) :- pos(rest2,R).

% --- Option conditions ---
% A: optometrist next to a restaurant
opt_next_rest :- pos(opt,O), rest(R), adjacent(O,R).
option(a) :- opt_next_rest.

% B: pharmacy next to veterinarian
pharm_next_vet :- pos(pharm,P), pos(vet,V), adjacent(P,V).
option(b) :- pharm_next_vet.

% C: a restaurant next to toy store
rest_next_toy :- pos(toy,T), rest(R), adjacent(T,R).
option(c) :- rest_next_toy.

% D: shoe store next to toy store (shoe is at 4)
shoe_next_toy :- pos(toy,3).
shoe_next_toy :- pos(toy,5).
option(d) :- shoe_next_toy.

% E: shoe store next to veterinarian
shoe_next_vet :- pos(vet,3).
shoe_next_vet :- pos(vet,5).
option(e) :- shoe_next_vet.

#show option/1.