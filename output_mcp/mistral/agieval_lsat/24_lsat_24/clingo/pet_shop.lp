% Base domains
kitten(himalayan; manx; siamese).
puppy(greyhound; newfoundland; rottweiler).
day(1..7).

% Exactly one kitten and one puppy featured each day
1 { featured_day(D, K, P) : kitten(K), puppy(P) } 1 :- day(D).

% Greyhounds are featured on day 1
featured_day(1, K, greyhound) :- kitten(K).

% No breed is featured on two consecutive days
:- featured_day(D, K, _), featured_day(D+1, K, _), day(D), D < 7.
:- featured_day(D, _, P), featured_day(D+1, _, P), day(D), D < 7.

% Any breed featured on day 1 is not featured on day 7
:- featured_day(1, K, _), featured_day(7, K, _).
:- featured_day(1, _, P), featured_day(7, _, P).

% Himalayans are featured on exactly three days, but not on day 1
:- #count { D : featured_day(D, himalayan, _) } != 3.
:- featured_day(1, himalayan, _).

% Rottweilers are not featured on day 7, nor on any day that features Himalayans
:- featured_day(7, _, rottweiler).
:- featured_day(D, himalayan, _), featured_day(D, _, rottweiler).

% Himalayans are not featured on day 7 (explicitly given in the question)
:- featured_day(7, himalayan, _).

% --- Answer choice conditions ---
% (A) Greyhounds are featured on days 3 and 5
option(a) :- featured_day(3, _, greyhound), featured_day(5, _, greyhound).

% (B) Newfoundlands are featured on day 3
option(b) :- featured_day(3, _, newfoundland).

% (C) Rottweilers are featured on day 6
option(c) :- featured_day(6, _, rottweiler).

% (D) Rottweilers are featured only on day 3
option(d) :- featured_day(3, _, rottweiler),
             not featured_day(1, _, rottweiler),
             not featured_day(2, _, rottweiler),
             not featured_day(4, _, rottweiler),
             not featured_day(5, _, rottweiler),
             not featured_day(6, _, rottweiler),
             not featured_day(7, _, rottweiler).

% (E) Rottweilers are featured on exactly three days
option(e) :- #count { D : featured_day(D, _, rottweiler) } = 3.

#show option/1.