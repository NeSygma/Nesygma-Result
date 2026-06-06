% Domains
day(1..7).
kitten(himalayan; manx; siamese).
puppy(greyhound; newfoundland; rottweiler).

% Each day has exactly one kitten and one puppy
1 { assign_kitten(D, K) : kitten(K) } 1 :- day(D).
1 { assign_puppy(D, P) : puppy(P) } 1 :- day(D).

% Constraint 1: Greyhounds are featured on day 1
assign_puppy(1, greyhound).

% Constraint 2: No breed is featured on any two consecutive days
:- assign_kitten(D1, K), assign_kitten(D2, K), D2 = D1+1.
:- assign_puppy(D1, P), assign_puppy(D2, P), D2 = D1+1.

% Constraint 3: Any breed featured on day 1 is not featured on day 7
:- assign_kitten(1, K), assign_kitten(7, K).
:- assign_puppy(1, P), assign_puppy(7, P).

% Constraint 4: Himalayans are featured on exactly three days, but not on day 1
:- assign_kitten(1, himalayan).
3 { assign_kitten(D, himalayan) : day(D) } 3.

% Constraint 5: Rottweilers are not featured on day 7, nor on any day that features Himalayans
:- assign_puppy(7, rottweiler).
:- assign_puppy(D, rottweiler), assign_kitten(D, himalayan).

% Helper predicates
featured_kitten(D, K) :- assign_kitten(D, K).
featured_puppy(D, P) :- assign_puppy(D, P).

% Count how many days each breed is featured
kitten_count(K, N) :- kitten(K), N = #count{D : assign_kitten(D, K)}.
puppy_count(P, N) :- puppy(P), N = #count{D : assign_puppy(D, P)}.

% Option A: There are exactly four breeds that are each featured on three days.
% Count breeds (both kitten and puppy) that are featured exactly 3 days
breed_three_days(N) :- N = #count{B : kitten(B), kitten_count(B, 3); B : puppy(B), puppy_count(B, 3)}.
option(a) :- breed_three_days(4).

% Option B: Greyhounds are featured on every day that Himalayans are.
% For all days D, if Himalayans are featured on D, then Greyhounds are featured on D
greyhound_on_himalayan_days :- day(D), assign_kitten(D, himalayan), assign_puppy(D, greyhound).
not_greyhound_on_himalayan_day :- day(D), assign_kitten(D, himalayan), not assign_puppy(D, greyhound).
option(b) :- not not_greyhound_on_himalayan_day.

% Option C: Himalayans are featured on every day that Greyhounds are.
% For all days D, if Greyhounds are featured on D, then Himalayans are featured on D
himalayan_on_greyhound_days :- day(D), assign_puppy(D, greyhound), assign_kitten(D, himalayan).
not_himalayan_on_greyhound_day :- day(D), assign_puppy(D, greyhound), not assign_kitten(D, himalayan).
option(c) :- not not_himalayan_on_greyhound_day.

% Option D: Himalayans are featured on every day that Rottweilers are not.
% For all days D, if Rottweilers are not featured on D, then Himalayans are featured on D
himalayan_on_non_rottweiler_days :- day(D), not assign_puppy(D, rottweiler), assign_kitten(D, himalayan).
not_himalayan_on_non_rottweiler_day :- day(D), not assign_puppy(D, rottweiler), not assign_kitten(D, himalayan).
option(d) :- not not_himalayan_on_non_rottweiler_day.

% Option E: Rottweilers are featured on every day that Himalayans are not.
% For all days D, if Himalayans are not featured on D, then Rottweilers are featured on D
rottweiler_on_non_himalayan_days :- day(D), not assign_kitten(D, himalayan), assign_puppy(D, rottweiler).
not_rottweiler_on_non_himalayan_day :- day(D), not assign_kitten(D, himalayan), not assign_puppy(D, rottweiler).
option(e) :- not not_rottweiler_on_non_himalayan_day.

#show option/1.