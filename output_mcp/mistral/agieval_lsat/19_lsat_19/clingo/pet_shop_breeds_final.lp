% Days
day(1..7).

% Kitten breeds
kitten(himalayan; manx; siamese).

% Puppy breeds
puppy(greyhound; newfoundland; rottweiler).

% Each day has exactly one kitten and one puppy
1 { kitten_on_day(K, D) : kitten(K) } 1 :- day(D).
1 { puppy_on_day(P, D) : puppy(P) } 1 :- day(D).

% Day 1 puppy is greyhound
puppy_on_day(greyhound, 1).

% Himalayans are featured on exactly three days, but not on day 1
:- { kitten_on_day(himalayan, D) : day(D), D != 1 } != 3.
:- kitten_on_day(himalayan, 1).

% Rottweilers are not featured on day 7
:- puppy_on_day(rottweiler, 7).

% Rottweilers are not featured on any day that features Himalayans
:- puppy_on_day(rottweiler, D), kitten_on_day(himalayan, D).

% No breed is featured on any two consecutive days
:- kitten_on_day(B, D), kitten_on_day(B, D+1), day(D), D < 7.
:- puppy_on_day(B, D), puppy_on_day(B, D+1), day(D), D < 7.

% Any breed featured on day 1 is not featured on day 7
:- kitten_on_day(B, 1), kitten_on_day(B, 7).
:- puppy_on_day(B, 1), puppy_on_day(B, 7).

% Define the kitten sequences for each option
% Option A: Himalayan, Manx, Siamese, Himalayan, Manx, Himalayan, Siamese
option_a :- kitten_on_day(himalayan, 1), kitten_on_day(manx, 2), kitten_on_day(siamese, 3),
             kitten_on_day(himalayan, 4), kitten_on_day(manx, 5), kitten_on_day(himalayan, 6),
             kitten_on_day(siamese, 7).

% Option B: Manx, Himalayan, Siamese, Himalayan, Manx, Himalayan, Manx
option_b :- kitten_on_day(manx, 1), kitten_on_day(himalayan, 2), kitten_on_day(siamese, 3),
             kitten_on_day(himalayan, 4), kitten_on_day(manx, 5), kitten_on_day(himalayan, 6),
             kitten_on_day(manx, 7).

% Option C: Manx, Himalayan, Manx, Himalayan, Siamese, Manx, Siamese
option_c :- kitten_on_day(manx, 1), kitten_on_day(himalayan, 2), kitten_on_day(manx, 3),
             kitten_on_day(himalayan, 4), kitten_on_day(siamese, 5), kitten_on_day(manx, 6),
             kitten_on_day(siamese, 7).

% Option D: Siamese, Himalayan, Manx, Himalayan, Siamese, Siamese, Himalayan
option_d :- kitten_on_day(siamese, 1), kitten_on_day(himalayan, 2), kitten_on_day(manx, 3),
             kitten_on_day(himalayan, 4), kitten_on_day(siamese, 5), kitten_on_day(siamese, 6),
             kitten_on_day(himalayan, 7).

% Option E: Siamese, Himalayan, Siamese, Himalayan, Manx, Siamese, Himalayan
option_e :- kitten_on_day(siamese, 1), kitten_on_day(himalayan, 2), kitten_on_day(siamese, 3),
             kitten_on_day(himalayan, 4), kitten_on_day(manx, 5), kitten_on_day(siamese, 6),
             kitten_on_day(himalayan, 7).

% Ensure only one option is true at a time
:- option_a, option_b.
:- option_a, option_c.
:- option_a, option_d.
:- option_a, option_e.
:- option_b, option_c.
:- option_b, option_d.
:- option_b, option_e.
:- option_c, option_d.
:- option_c, option_e.
:- option_d, option_e.

% Map the correct answer to option/1
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.