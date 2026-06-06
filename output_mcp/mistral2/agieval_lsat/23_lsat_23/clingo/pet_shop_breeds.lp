% Define the days and breeds
% Days: 1 to 7
 day(1..7).

% Breeds of kittens
kitten_breed(himalayan).
kitten_breed(manx).
kitten_breed(siamese).

% Breeds of puppies
puppy_breed(greyhound).
puppy_breed(newfoundland).
puppy_breed(rottweiler).

% Each day features exactly one kitten breed and one puppy breed
1 { featured_kitten(D, K) : kitten_breed(K) } 1 :- day(D).
1 { featured_puppy(D, P) : puppy_breed(P) } 1 :- day(D).

% Greyhounds are featured on day 1
:- not featured_puppy(1, greyhound).

% No breed is featured on any two consecutive days
:- day(D), day(D+1), D < 7,
   featured_kitten(D, K), featured_kitten(D+1, K).
:- day(D), day(D+1), D < 7,
   featured_puppy(D, P), featured_puppy(D+1, P).

% Any breed featured on day 1 is not featured on day 7
:- featured_kitten(1, K), featured_kitten(7, K).
:- featured_puppy(1, P), featured_puppy(7, P).

% Himalayans are featured on exactly three days, but not on day 1
:- { featured_kitten(D, himalayan) : day(D) } != 3.
:- featured_kitten(1, himalayan).

% Rottweilers are not featured on day 7
:- featured_puppy(7, rottweiler).

% Rottweilers are not featured on any day that features Himalayans
:- day(D), featured_kitten(D, himalayan), featured_puppy(D, rottweiler).

% Count the number of days each breed is featured
count_kitten(K, N) :- N = #count { D : featured_kitten(D, K) }.
count_puppy(P, N) :- N = #count { D : featured_puppy(D, P) }.

% Define helper predicates for the answer conditions
% (A) There are exactly four breeds that are each featured on three days.
four_breeds_three_days :- 4 = #count { B : count_kitten(B, 3) } + #count { B : count_puppy(B, 3) }.

% (B) Greyhounds are featured on every day that Himalayans are.
:- day(D), featured_kitten(D, himalayan), not featured_puppy(D, greyhound).
answer_b :- not (day(D) : featured_kitten(D, himalayan), not featured_puppy(D, greyhound)).

% (C) Himalayans are featured on every day that Greyhounds are.
:- day(D), featured_puppy(D, greyhound), not featured_kitten(D, himalayan).
answer_c :- not (day(D) : featured_puppy(D, greyhound), not featured_kitten(D, himalayan)).

% (D) Himalayans are featured on every day that Rottweilers are not.
:- day(D), not featured_puppy(D, rottweiler), not featured_kitten(D, himalayan).
answer_d :- not (day(D) : not featured_puppy(D, rottweiler), not featured_kitten(D, himalayan)).

% (E) Rottweilers are featured on every day that Himalayans are not.
:- day(D), not featured_kitten(D, himalayan), not featured_puppy(D, rottweiler).
answer_e :- not (day(D) : not featured_kitten(D, himalayan), not featured_puppy(D, rottweiler)).

% Map the correct answer to option/1
option(a) :- four_breeds_three_days.
option(b) :- answer_b.
option(c) :- answer_c.
option(d) :- answer_d.
option(e) :- answer_e.

#show option/1.