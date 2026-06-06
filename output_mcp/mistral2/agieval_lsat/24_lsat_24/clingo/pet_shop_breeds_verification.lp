% Verify that option(d) is the only possible correct answer

% Define the days and breeds
 day(1..7).
 kitten_breed(himalayan; manx; siamese).
 puppy_breed(greyhound; newfoundland; rottweiler).

% Each day features exactly one kitten breed and one puppy breed
1 { featured_kitten(D, K) : kitten_breed(K) } 1 :- day(D).
1 { featured_puppy(D, P) : puppy_breed(P) } 1 :- day(D).

% Greyhounds are featured on day 1
:- not featured_puppy(1, greyhound).

% No breed is featured on any two consecutive days
:- featured_kitten(D, K), featured_kitten(D+1, K), D < 7.
:- featured_puppy(D, P), featured_puppy(D+1, P), D < 7.

% Any breed featured on day 1 is not featured on day 7
:- featured_kitten(1, K), featured_kitten(7, K).
:- featured_puppy(1, P), featured_puppy(7, P).

% Himalayans are featured on exactly three days, but not on day 1
:- #count { D : featured_kitten(D, himalayan) } != 3.
:- featured_kitten(1, himalayan).

% Rottweilers are not featured on day 7, nor on any day that features Himalayans
:- featured_puppy(7, rottweiler).
:- featured_puppy(D, rottweiler), featured_kitten(D, himalayan).

% Himalayans are not featured on day 7 (additional constraint from the question)
:- featured_kitten(7, himalayan).

% Define helper predicates for the options
% (A) Greyhounds are featured on days 3 and 5
option_a :- featured_puppy(3, greyhound), featured_puppy(5, greyhound).

% (B) Newfoundlands are featured on day 3
option_b :- featured_puppy(3, newfoundland).

% (C) Rottweilers are featured on day 6
option_c :- featured_puppy(6, rottweiler).

% (D) Rottweilers are featured only on day 3
option_d :- featured_puppy(3, rottweiler),
            not featured_puppy(1, rottweiler),
            not featured_puppy(2, rottweiler),
            not featured_puppy(4, rottweiler),
            not featured_puppy(5, rottweiler),
            not featured_puppy(6, rottweiler),
            not featured_puppy(7, rottweiler).

% (E) Rottweilers are featured on exactly three days
option_e :- #count { D : featured_puppy(D, rottweiler) } = 3.

% Ensure only one option is true
1 { selected_option(a); selected_option(b); selected_option(c); selected_option(d); selected_option(e) } 1.

% Map the selected option to option/1
option(X) :- selected_option(X).

#show option/1.