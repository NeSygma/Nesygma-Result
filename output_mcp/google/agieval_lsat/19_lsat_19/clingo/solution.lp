% Days
day(1..7).

% Breeds
kitten(himalayan; manx; siamese).
puppy(greyhound; newfoundland; rottweiler).

% Define options
is_option(a, 1, himalayan). is_option(a, 2, manx). is_option(a, 3, siamese). is_option(a, 4, himalayan). is_option(a, 5, manx). is_option(a, 6, himalayan). is_option(a, 7, siamese).
is_option(b, 1, manx). is_option(b, 2, himalayan). is_option(b, 3, siamese). is_option(b, 4, himalayan). is_option(b, 5, manx). is_option(b, 6, himalayan). is_option(b, 7, manx).
is_option(c, 1, manx). is_option(c, 2, himalayan). is_option(c, 3, manx). is_option(c, 4, himalayan). is_option(c, 5, siamese). is_option(c, 6, manx). is_option(c, 7, siamese).
is_option(d, 1, siamese). is_option(d, 2, himalayan). is_option(d, 3, manx). is_option(d, 4, himalayan). is_option(d, 5, siamese). is_option(d, 6, siamese). is_option(d, 7, himalayan).
is_option(e, 1, siamese). is_option(e, 2, himalayan). is_option(e, 3, siamese). is_option(e, 4, himalayan). is_option(e, 5, manx). is_option(e, 6, siamese). is_option(e, 7, himalayan).

% Select an option to test
{ selected_option(O) } = 1 :- option_id(O).
option_id(a;b;c;d;e).

% Assign kittens based on selected option
kitten_on(D, K) :- selected_option(O), is_option(O, D, K).

% Constraints on kittens
% 1. No breed is featured on any two consecutive days.
:- kitten_on(D, K), kitten_on(D+1, K).
% 2. Any breed featured on day 1 is not featured on day 7.
:- kitten_on(1, K), kitten_on(7, K).
% 3. Himalayans are featured on exactly three days, but not on day 1.
:- not #count { D : kitten_on(D, himalayan) } = 3.
:- kitten_on(1, himalayan).

% Puppy assignments
1 { puppy_on(D, P) : puppy(P) } 1 :- day(D).

% Condition 1: Greyhounds on day 1.
:- not puppy_on(1, greyhound).
% Condition 2: No puppy breed on consecutive days.
:- puppy_on(D, P), puppy_on(D+1, P).
% Condition 3: Puppy breed on day 1 != day 7.
:- puppy_on(1, P), puppy_on(7, P).
% Condition 6: Rottweilers not on day 7.
:- puppy_on(7, rottweiler).
% Condition 7: Rottweilers not on any day with Himalayans.
:- puppy_on(D, rottweiler), kitten_on(D, himalayan).

option(O) :- selected_option(O).
#show option/1.