% Domains
day(1..7).
kitten(himalayan; manx; siamese).
puppy(greyhound; newfoundland; rottweiler).

% Choice rules: assign exactly one kitten and one puppy per day
1 { kitten(D, K) : kitten(K) } 1 :- day(D).
1 { puppy(D, P) : puppy(P) } 1 :- day(D).

% Condition 1: Greyhounds are featured on day 1
puppy(1, greyhound).

% Condition 2: No breed is featured on any two consecutive days
:- kitten(D, K), kitten(D+1, K), day(D), day(D+1).
:- puppy(D, P), puppy(D+1, P), day(D), day(D+1).

% Condition 3: Any breed featured on day 1 is not featured on day 7
:- kitten(1, K), kitten(7, K).
:- puppy(1, P), puppy(7, P).

% Condition 4: Himalayans are featured on exactly three days, but not on day 1
3 { kitten(D, himalayan) : day(D) } 3.
:- kitten(1, himalayan).

% Condition 5: Rottweilers are not featured on day 7, nor on any day that features Himalayans
:- puppy(7, rottweiler).
:- puppy(D, rottweiler), kitten(D, himalayan).

% Additional condition from question: Himalayans are not featured on day 7
:- kitten(7, himalayan).

% Define conditions for each option
% Option A: Greyhounds are featured on days 3 and 5
cond_a :- puppy(3, greyhound), puppy(5, greyhound).

% Option B: Newfoundlands are featured on day 3
cond_b :- puppy(3, newfoundland).

% Option C: Rottweilers are featured on day 6
cond_c :- puppy(6, rottweiler).

% Option D: Rottweilers are featured only on day 3
cond_d :- puppy(3, rottweiler), not puppy(D, rottweiler) : day(D), D != 3.

% Option E: Rottweilers are featured on exactly three days
cond_e :- 3 { puppy(D, rottweiler) : day(D) } 3.

% Track which options are possible
possible_a :- cond_a.
possible_b :- cond_b.
possible_c :- cond_c.
possible_d :- cond_d.
possible_e :- cond_e.

% Show which options are possible
#show possible_a/0.
#show possible_b/0.
#show possible_c/0.
#show possible_d/0.
#show possible_e/0.