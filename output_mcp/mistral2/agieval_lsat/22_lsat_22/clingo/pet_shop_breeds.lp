% Define the days and breeds
% Days: 1 to 7
 day(1..7).

% Kitten breeds
kitten_breed(himalayan).
kitten_breed(manx).
kitten_breed(siamese).

% Puppy breeds
puppy_breed(greyhound).
puppy_breed(newfoundland).
puppy_breed(rottweiler).

% Assign exactly one kitten breed per day
1 { kitten(D, B) : kitten_breed(B) } 1 :- day(D).

% Assign exactly one puppy breed per day
1 { puppy(D, B) : puppy_breed(B) } 1 :- day(D).

% Greyhounds are featured on day 1
:- not puppy(1, greyhound).

% No breed is featured on any two consecutive days
:- kitten(D, B), kitten(D+1, B).
:- puppy(D, B), puppy(D+1, B).

% Any breed featured on day 1 is not featured on day 7
:- kitten(1, B), kitten(7, B).
:- puppy(1, B), puppy(7, B).

% Himalayans are featured on exactly three days, but not on day 1
:- { kitten(D, himalayan) : day(D) } != 3.
:- kitten(1, himalayan).

% Rottweilers are not featured on day 7
:- puppy(7, rottweiler).

% Rottweilers are not featured on any day that features Himalayans
:- puppy(D, rottweiler), kitten(D, himalayan).

% Himalayans are not featured on day 7 (given in the question)
:- kitten(7, himalayan).

% Additional constraint: Himalayans are featured on exactly three days (already enforced above)

% Define the pairs of days to check for the multiple-choice question
% We need to check if the same kitten and puppy breeds are featured on the pairs of days

% Helper predicates to check if the same kitten breed is featured on two days
same_kitten(D1, D2) :- kitten(D1, B), kitten(D2, B), D1 < D2.

% Helper predicates to check if the same puppy breed is featured on two days
same_puppy(D1, D2) :- puppy(D1, B), puppy(D2, B), D1 < D2.

% Helper predicate to check if both the same kitten and puppy breeds are featured on two days
same_both(D1, D2) :- same_kitten(D1, D2), same_puppy(D1, D2).

% Define the pairs of days from the options
pair(1, 3).
pair(2, 6).
pair(3, 5).
pair(4, 6).
pair(5, 7).

% Check if the pair of days cannot feature both the same kitten and puppy breeds
% We want to find the pair that CANNOT feature both the same breeds
% So we will derive a predicate that indicates a pair is invalid (i.e., cannot have same breeds)
invalid_pair(D1, D2) :- pair(D1, D2), same_both(D1, D2).

% The correct answer is the pair that is NOT invalid (i.e., cannot have same breeds)
% So we will map the options to the pairs and check which one is not invalid

% Map the pairs to the options
option(a) :- invalid_pair(1, 3), not invalid_pair(2, 6), not invalid_pair(3, 5), not invalid_pair(4, 6), not invalid_pair(5, 7).
option(b) :- invalid_pair(2, 6), not invalid_pair(1, 3), not invalid_pair(3, 5), not invalid_pair(4, 6), not invalid_pair(5, 7).
option(c) :- invalid_pair(3, 5), not invalid_pair(1, 3), not invalid_pair(2, 6), not invalid_pair(4, 6), not invalid_pair(5, 7).
option(d) :- invalid_pair(4, 6), not invalid_pair(1, 3), not invalid_pair(2, 6), not invalid_pair(3, 5), not invalid_pair(5, 7).
option(e) :- invalid_pair(5, 7), not invalid_pair(1, 3), not invalid_pair(2, 6), not invalid_pair(3, 5), not invalid_pair(4, 6).

#show option/1.