% Define the days and breeds
% Days: 1 to 7
 day(1..7).

% Breeds of kittens
kitten_breed(himalayan; manx; siamese).

% Breeds of puppies
puppy_breed(greyhound; newfoundland; rottweiler).

% Featured breeds on each day
% We use choice rules to allow the solver to assign breeds to days
{ featured_kitten(D, K) : kitten_breed(K) } 1 :- day(D).
{ featured_puppy(D, P) : puppy_breed(P) } 1 :- day(D).

% Constraints

% 1. Greyhounds are featured on day 1
:- featured_puppy(1, P), P != greyhound.

% 2. No breed is featured on any two consecutive days
:- featured_kitten(D, K), featured_kitten(D+1, K).
:- featured_puppy(D, P), featured_puppy(D+1, P).

% Ensure we do not exceed the last day
:- day(D), D < 7, featured_kitten(D+1, _), featured_puppy(D+1, _).

% 3. Any breed featured on day 1 is not featured on day 7
% For kittens
:- featured_kitten(1, K), featured_kitten(7, K).
% For puppies
:- featured_puppy(1, P), featured_puppy(7, P).

% 4. Himalayans are featured on exactly three days, but not on day 1
:- featured_kitten(D, himalayan), D == 1.
% Count Himalayans
num_himalayan_days(N) :- N = #count{ D : featured_kitten(D, himalayan) }.
:- num_himalayan_days(N), N != 3.

% 5. Rottweilers are not featured on day 7, nor on any day that features Himalayans
:- featured_puppy(7, rottweiler).
:- featured_puppy(D, rottweiler), featured_kitten(D, himalayan).

% Additional constraint: Ensure that each day has exactly one kitten and one puppy
% This is already enforced by the choice rules above.

% --- Multiple Choice Options ---
% We need to check which of the options (A) through (E) could be true.
% We will define conditions for each option and map them to option/1.

% Option A: Greyhounds and Siamese are both featured on day 2
option(a) :- featured_puppy(2, greyhound), featured_kitten(2, siamese).

% Option B: Greyhounds and Himalayans are both featured on day 7
option(b) :- featured_puppy(7, greyhound), featured_kitten(7, himalayan).

% Option C: Rottweilers and Himalayans are both featured on day 4
option(c) :- featured_puppy(4, rottweiler), featured_kitten(4, himalayan).

% Option D: Rottweilers and Manx are both featured on day 5
option(d) :- featured_puppy(5, rottweiler), featured_kitten(5, manx).

% Option E: Newfoundlands and Manx are both featured on day 6
option(e) :- featured_puppy(6, newfoundland), featured_kitten(6, manx).

#show option/1.