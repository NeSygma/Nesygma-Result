% Time horizon
day(1..7).

% Breeds
kitten(himalayan; manx; siamese).
puppy(greyhound; newfoundland; rottweiler).

% Base facts about features
1 { featured_day(D, K, P) : kitten(K), puppy(P) } 1 :- day(D).

% Extract kitten and puppy features for each day
kitten_day(D, K) :- featured_day(D, K, _).
puppy_day(D, P) :- featured_day(D, _, P).

% Greyhounds are featured on day 1 (puppies)
:- not puppy_day(1, greyhound).

% No breed is featured on any two consecutive days
% For kittens: no kitten breed appears on two consecutive days
:- kitten_day(D, K), kitten_day(D+1, K), day(D), day(D+1).
% For puppies: no puppy breed appears on two consecutive days
:- puppy_day(D, P), puppy_day(D+1, P), day(D), day(D+1).

% Any breed featured on day 1 is not featured on day 7
% This applies to both kittens and puppies
:- kitten_day(1, K), kitten_day(7, K).
:- puppy_day(1, P), puppy_day(7, P).

% Himalayans are featured on exactly three days, but not on day 1
:- { kitten_day(D, himalayan) } != 3.
:- kitten_day(1, himalayan).

% Rottweilers are not featured on day 7, nor on any day that features Himalayans
:- puppy_day(7, rottweiler).
:- puppy_day(D, rottweiler), kitten_day(D, himalayan).

% Himalayans are not featured on day 2 (from the question condition)
:- kitten_day(2, himalayan).

% Define the conditions for each option
% We need to check which COULD be true, so we'll derive option(X) if the condition is possible

% Option A: Manx are featured on day 3
% This is possible if kitten_day(3, manx) is true
% We'll check if this leads to a consistent solution

% Option B: Siamese are featured on day 4
% This is possible if kitten_day(4, siamese) is true

% Option C: Rottweilers are featured on day 5
% This is possible if puppy_day(5, rottweiler) is true

% Option D: Himalayans are featured on day 6
% This is possible if kitten_day(6, himalayan) is true

% Option E: Greyhounds are featured on day 7
% This is possible if puppy_day(7, greyhound) is true

% Instead of trying to derive option(X) directly, let's check each option
% by adding it as a constraint and seeing if a solution exists

% We'll use a choice rule to select which option to check
{ check_option(A) : option_id(A) } 1.

% Define option_id for each choice
option_id(a; b; c; d; e).

% Define what each option means
option_means(a, kitten_day(3, manx)).
option_means(b, kitten_day(4, siamese)).
option_means(c, puppy_day(5, rottweiler)).
option_means(d, kitten_day(6, himalayan)).
option_means(e, puppy_day(7, greyhound)).

% If we're checking an option, add it as a constraint
:- check_option(A), not option_means(A, Condition), Condition.

% Map the correct answer to option/1 (MANDATORY)
% The answer is the option that is possible (i.e., for which a solution exists)
answer(A) :- check_option(A), not inconsistent(A).
inconsistent(A) :- check_option(A), not option_means(A, Condition), Condition.

% Show the answer
#show answer/1.

% Show the full solution for debugging
#show featured_day/3.
#show kitten_day/2.
#show puppy_day/2.