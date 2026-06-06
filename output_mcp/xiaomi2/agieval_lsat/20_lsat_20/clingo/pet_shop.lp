% Domains
day(1..7).
kitten_breed(himalayan; manx; siamese).
puppy_breed(greyhound; newfoundland; rottweiler).

% Choice rules for assignments
{ kitten(Day, Breed) : kitten_breed(Breed) } 1 :- day(Day).
{ puppy(Day, Breed) : puppy_breed(Breed) } 1 :- day(Day).

% Constraints
% 1. Greyhound on day 1
puppy(1, greyhound).

% 2. No breed on consecutive days
:- kitten(Day1, Breed), kitten(Day2, Breed), Day2 = Day1+1.
:- puppy(Day1, Breed), puppy(Day2, Breed), Day2 = Day1+1.

% 3. Any breed on day 1 not on day 7
:- kitten(1, Breed), kitten(7, Breed).
:- puppy(1, Breed), puppy(7, Breed).

% 4. Himalayan exactly 3 days, not day 1
:- kitten(1, himalayan).
3 { kitten(Day, himalayan) : day(Day) } 3.

% 5. Rottweiler not on day 7, and not on any day with Himalayan
:- puppy(7, rottweiler).
:- puppy(Day, rottweiler), kitten(Day, himalayan).

% Additional: Himalayan not on day 2
:- kitten(2, himalayan).

% Define possible options
possible_a :- kitten(3, manx).
possible_b :- kitten(4, siamese).
possible_c :- puppy(5, rottweiler).
possible_d :- kitten(6, himalayan).
possible_e :- puppy(7, greyhound).

% Define option if possible
option(a) :- possible_a.
option(b) :- possible_b.
option(c) :- possible_c.
option(d) :- possible_d.
option(e) :- possible_e.

% Select exactly one option that is possible
1 { selected(X) : option(X) } 1.

% Show selected option as option/1
option(X) :- selected(X).

#show option/1.