% Days
day(1..7).

% Breeds
kitten(himalayan; manx; siamese).
puppy(greyhound; newfoundland; rottweiler).

% Base facts
puppy(greyhound, 1).

% Choice rules for assignments
1 { kitten_on_day(K, D) : kitten(K) } 1 :- day(D).
1 { puppy_on_day(P, D) : puppy(P) } 1 :- day(D).

% No consecutive same breed for kittens
:- kitten_on_day(K, D), kitten_on_day(K, D+1), D < 7.

% No consecutive same breed for puppies
:- puppy_on_day(P, D), puppy_on_day(P, D+1), D < 7.

% Day 1 breeds cannot be on day 7
:- kitten_on_day(K, 1), kitten_on_day(K, 7).
:- puppy_on_day(P, 1), puppy_on_day(P, 7).

% Himalayans on exactly 3 days, not on day 1
himalayan_days(D) :- kitten_on_day(himalayan, D).
himalayan_count(N) :- N = #count{ D : himalayan_days(D) }.
:- himalayan_count(N), N != 3.
:- kitten_on_day(himalayan, 1).

% Rottweilers not on day 7, and not on any day with Himalayans
:- puppy_on_day(rottweiler, 7).
:- puppy_on_day(rottweiler, D), himalayan_days(D).

% Define the options as possible scenarios
% Option A: Greyhounds and Siamese on day 2
% This would require greyhounds on day 2, but greyhounds are on day 1 and cannot be consecutive
possible_a :- puppy_on_day(greyhound, 2), kitten_on_day(siamese, 2).

% Option B: Greyhounds and Himalayans on day 7
% Greyhounds cannot be on day 7 because they're on day 1 (constraint 3)
possible_b :- puppy_on_day(greyhound, 7), kitten_on_day(himalayan, 7).

% Option C: Rottweilers and Himalayans on day 4
% Rottweilers cannot be on Himalayan days (constraint 5)
possible_c :- puppy_on_day(rottweiler, 4), kitten_on_day(himalayan, 4).

% Option D: Rottweilers and Manx on day 5
possible_d :- puppy_on_day(rottweiler, 5), kitten_on_day(manx, 5).

% Option E: Newfoundlands and Manx on day 6
possible_e :- puppy_on_day(newfoundland, 6), kitten_on_day(manx, 6).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- possible_a, not possible_b, not possible_c, not possible_d, not possible_e.
option(b) :- possible_b, not possible_a, not possible_c, not possible_d, not possible_e.
option(c) :- possible_c, not possible_a, not possible_b, not possible_d, not possible_e.
option(d) :- possible_d, not possible_a, not possible_b, not possible_c, not possible_e.
option(e) :- possible_e, not possible_a, not possible_b, not possible_c, not possible_d.

#show option/1.