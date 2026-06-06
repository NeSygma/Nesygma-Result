% Domains
day(1..7).
kitten_breed(himalayan; manx; siamese).
puppy_breed(greyhound; newfoundland; rottweiler).

% Choice: exactly one kitten and one puppy per day
{ kitten(D, B) : kitten_breed(B) } 1 :- day(D).
{ puppy(D, B) : puppy_breed(B) } 1 :- day(D).

% Constraint 1: Greyhounds featured on day 1
puppy(1, greyhound).

% Constraint 2: No breed featured on two consecutive days
:- kitten(D, B), kitten(D+1, B), day(D), day(D+1).
:- puppy(D, B), puppy(D+1, B), day(D), day(D+1).

% Constraint 3: Any breed on day 1 not featured on day 7
:- kitten(1, B), kitten(7, B).
:- puppy(1, B), puppy(7, B).

% Constraint 4: Himalayans on exactly 3 days, not on day 1
:- kitten(1, himalayan).
3 { kitten(D, himalayan) : day(D) } 3.

% Constraint 5: Rottweilers not on day 7, nor on any day with Himalayans
:- puppy(7, rottweiler).
:- puppy(D, rottweiler), kitten(D, himalayan).

% Check each option
check_a :- puppy(2, greyhound), kitten(2, siamese).
check_b :- puppy(7, greyhound), kitten(7, himalayan).
check_c :- puppy(4, rottweiler), kitten(4, himalayan).
check_d :- puppy(5, rottweiler), kitten(5, manx).
check_e :- puppy(6, newfoundland), kitten(6, manx).

option(a) :- check_a.
option(b) :- check_b.
option(c) :- check_c.
option(d) :- check_d.
option(e) :- check_e.

#show option/1.