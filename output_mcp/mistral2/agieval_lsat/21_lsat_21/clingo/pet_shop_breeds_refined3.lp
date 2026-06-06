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
:- featured_kitten(D, K), featured_kitten(D+1, K), day(D+1).
:- featured_puppy(D, P), featured_puppy(D+1, P), day(D+1).

% 3. Any breed featured on day 1 is not featured on day 7
% For kittens
:- featured_kitten(1, K), featured_kitten(7, K).
% For puppies
:- featured_puppy(1, P), featured_puppy(7, P).

% 4. Himalayans are featured on exactly three days, but not on day 1
:- featured_kitten(1, himalayan).
% Count Himalayans
num_himalayan_days(N) :- N = #count{ D : featured_kitten(D, himalayan) }.
:- num_himalayan_days(N), N != 3.

% 5. Rottweilers are not featured on day 7, nor on any day that features Himalayans
:- featured_puppy(7, rottweiler).
:- featured_puppy(D, rottweiler), featured_kitten(D, himalayan), day(D).

% --- Multiple Choice Options ---
% We will check each option individually to see if it could be true.

% Option A: Greyhounds and Siamese are both featured on day 2
option_a :- featured_puppy(2, greyhound), featured_kitten(2, siamese).

% Option B: Greyhounds and Himalayans are both featured on day 7
option_b :- featured_puppy(7, greyhound), featured_kitten(7, himalayan).

% Option C: Rottweilers and Himalayans are both featured on day 4
option_c :- featured_puppy(4, rottweiler), featured_kitten(4, himalayan).

% Option D: Rottweilers and Manx are both featured on day 5
option_d :- featured_puppy(5, rottweiler), featured_kitten(5, manx).

% Option E: Newfoundlands and Manx are both featured on day 6
option_e :- featured_puppy(6, newfoundland), featured_kitten(6, manx).

% Only one option can be true at a time (for checking)
1 { option_a ; option_b ; option_c ; option_d ; option_e } 1.

% Map the correct answer to option/1 (MANDATORY)
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.