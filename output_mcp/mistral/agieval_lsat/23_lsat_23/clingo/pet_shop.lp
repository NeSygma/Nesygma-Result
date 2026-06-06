% Domains
 day(1..7).
 kitten_breed(himalayan; manx; siamese).
 puppy_breed(greyhound; newfoundland; rottweiler).

% Assignments
1 { kitten(D, B) : kitten_breed(B) } 1 :- day(D).
1 { puppy(D, B) : puppy_breed(B) } 1 :- day(D).

% Constraints
% Greyhounds on day 1
puppy(1, greyhound).

% No breed on consecutive days
:- kitten(D, B), kitten(D+1, B), day(D), D < 7.
:- puppy(D, B), puppy(D+1, B), day(D), D < 7.

% Breed on day 1 not on day 7
:- kitten(1, B), kitten(7, B).
:- puppy(1, B), puppy(7, B).

% Himalayans on exactly 3 days, not on day 1
:- #count{D : kitten(D, himalayan)} != 3.
:- kitten(1, himalayan).

% Rottweilers not on day 7, nor on any day with Himalayans
:- puppy(7, rottweiler).
:- puppy(D, rottweiler), kitten(D, himalayan).

% Helper predicates for breed counts
kitten_count(B, N) :- N = #count{D : kitten(D, B)}.
puppy_count(B, N) :- N = #count{D : puppy(D, B)}.

% (A) There are exactly four breeds that are each featured on three days.
% This means exactly 4 breeds (out of 6) appear on exactly 3 days.
option(a) :- #count{B : kitten_count(B, 3) ; puppy_count(B, 3)} = 4.

% (B) Greyhounds are featured on every day that Himalayans are.
% This means: there is no day where Himalayans are featured but Greyhounds are not.
b_violated :- kitten(D, himalayan), not puppy(D, greyhound).
b_holds :- not b_violated.
option(b) :- b_holds.

% (C) Himalayans are featured on every day that Greyhounds are.
% This means: there is no day where Greyhounds are featured but Himalayans are not.
c_violated :- puppy(D, greyhound), not kitten(D, himalayan).
c_holds :- not c_violated.
option(c) :- c_holds.

% (D) Himalayans are featured on every day that Rottweilers are not.
% This means: there is no day where Rottweilers are not featured and Himalayans are not featured.
d_violated :- not puppy(D, rottweiler), not kitten(D, himalayan).
d_holds :- not d_violated.
option(d) :- d_holds.

% (E) Rottweilers are featured on every day that Himalayans are not.
% This means: there is no day where Himalayans are not featured and Rottweilers are not featured.
e_violated :- not kitten(D, himalayan), not puppy(D, rottweiler).
e_holds :- not e_violated.
option(e) :- e_holds.

#show option/1.