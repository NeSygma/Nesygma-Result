% Days
day(1..7).

% Kitten breeds
kitten_breed(himalayan).
kitten_breed(manx).
kitten_breed(siamese).

% Puppy breeds
puppy_breed(greyhound).
puppy_breed(newfoundland).
puppy_breed(rottweiler).

% Choice rules: exactly one kitten and one puppy per day
1 { kitten(D, B) : kitten_breed(B) } 1 :- day(D).
1 { puppy(D, B) : puppy_breed(B) } 1 :- day(D).

% Constraint 1: Greyhounds featured on day 1
:- not puppy(1, greyhound).

% Constraint 2: No breed featured on any two consecutive days (for kittens)
:- kitten(D, B), kitten(D+1, B), day(D), day(D+1).

% Constraint 2: No breed featured on any two consecutive days (for puppies)
:- puppy(D, B), puppy(D+1, B), day(D), day(D+1).

% Constraint 3: Any breed featured on day 1 is not featured on day 7
% For kittens
:- kitten(1, B), kitten(7, B).
% For puppies
:- puppy(1, B), puppy(7, B).

% Constraint 4: Himalayans featured on exactly three days, but not on day 1
himalayan_count(N) :- N = #count{D : kitten(D, himalayan)}.
:- himalayan_count(N), N != 3.
:- kitten(1, himalayan).

% Constraint 5: Rottweilers not featured on day 7, nor on any day that features Himalayans
:- puppy(7, rottweiler).
:- puppy(D, rottweiler), kitten(D, himalayan), day(D).

% Multiple choice options - kitten sequences
% Option A: Himalayan, Manx, Siamese, Himalayan, Manx, Himalayan, Siamese
option_a_sequence(1, himalayan).
option_a_sequence(2, manx).
option_a_sequence(3, siamese).
option_a_sequence(4, himalayan).
option_a_sequence(5, manx).
option_a_sequence(6, himalayan).
option_a_sequence(7, siamese).

% Option B: Manx, Himalayan, Siamese, Himalayan, Manx Himalayan, Manx
% Note: The problem statement seems to have a typo - "Manx Himalayan" likely means "Manx, Himalayan"
option_b_sequence(1, manx).
option_b_sequence(2, himalayan).
option_b_sequence(3, siamese).
option_b_sequence(4, himalayan).
option_b_sequence(5, manx).
option_b_sequence(6, himalayan).
option_b_sequence(7, manx).

% Option C: Manx, Himalayan, Manx, Himalayan, Siamese, Manx, Siamese
option_c_sequence(1, manx).
option_c_sequence(2, himalayan).
option_c_sequence(3, manx).
option_c_sequence(4, himalayan).
option_c_sequence(5, siamese).
option_c_sequence(6, manx).
option_c_sequence(7, siamese).

% Option D: Siamese, Himalayan, Manx, Himalayan, Siamese, Siamese, Himalayan
option_d_sequence(1, siamese).
option_d_sequence(2, himalayan).
option_d_sequence(3, manx).
option_d_sequence(4, himalayan).
option_d_sequence(5, siamese).
option_d_sequence(6, siamese).
option_d_sequence(7, himalayan).

% Option E: Siamese, Himalayan, Siamese, Himalayan, Manx, Siamese, Himalayan
option_e_sequence(1, siamese).
option_e_sequence(2, himalayan).
option_e_sequence(3, siamese).
option_e_sequence(4, himalayan).
option_e_sequence(5, manx).
option_e_sequence(6, siamese).
option_e_sequence(7, himalayan).

% Helper predicates for checking consecutive same breed in options
consecutive_same_a(D, B) :- option_a_sequence(D, B), option_a_sequence(D+1, B), day(D), day(D+1).
consecutive_same_b(D, B) :- option_b_sequence(D, B), option_b_sequence(D+1, B), day(D), day(D+1).
consecutive_same_c(D, B) :- option_c_sequence(D, B), option_c_sequence(D+1, B), day(D), day(D+1).
consecutive_same_d(D, B) :- option_d_sequence(D, B), option_d_sequence(D+1, B), day(D), day(D+1).
consecutive_same_e(D, B) :- option_e_sequence(D, B), option_e_sequence(D+1, B), day(D), day(D+1).

% Check if each option is consistent with the constraints
% Option A consistency
option_a :-
    % No consecutive same breed
    not consecutive_same_a(_, _),
    % Exactly 3 Himalayans
    #count{D : option_a_sequence(D, himalayan)} = 3,
    % Not Himalayan on day 1
    not option_a_sequence(1, himalayan),
    % Day 1 breed not on day 7
    not (option_a_sequence(1, B), option_a_sequence(7, B)).

% Option B consistency
option_b :-
    not consecutive_same_b(_, _),
    #count{D : option_b_sequence(D, himalayan)} = 3,
    not option_b_sequence(1, himalayan),
    not (option_b_sequence(1, B), option_b_sequence(7, B)).

% Option C consistency
option_c :-
    not consecutive_same_c(_, _),
    #count{D : option_c_sequence(D, himalayan)} = 3,
    not option_c_sequence(1, himalayan),
    not (option_c_sequence(1, B), option_c_sequence(7, B)).

% Option D consistency
option_d :-
    not consecutive_same_d(_, _),
    #count{D : option_d_sequence(D, himalayan)} = 3,
    not option_d_sequence(1, himalayan),
    not (option_d_sequence(1, B), option_d_sequence(7, B)).

% Option E consistency
option_e :-
    not consecutive_same_e(_, _),
    #count{D : option_e_sequence(D, himalayan)} = 3,
    not option_e_sequence(1, himalayan),
    not (option_e_sequence(1, B), option_e_sequence(7, B)).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.