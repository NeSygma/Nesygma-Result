% Domains
day(1..7).

kittenBreed(him). kittenBreed(man). kittenBreed(siam).
puppyBreed(grey). puppyBreed(new). puppyBreed(rot).

% Exactly one kitten breed per day
1 { kitten(K,D) : kittenBreed(K) } 1 :- day(D).
% Exactly one puppy breed per day
1 { puppy(P,D) : puppyBreed(P) } 1 :- day(D).

% Greyhounds on day 1
puppy(grey,1).

% No breed appears on consecutive days (kitten)
:- kitten(K,D), kitten(K,D1), D1 = D+1.
% No breed appears on consecutive days (puppy)
:- puppy(P,D), puppy(P,D1), D1 = D+1.

% Any breed on day1 not on day7
:- kitten(K,1), kitten(K,7).
:- puppy(P,1), puppy(P,7).

% Himalayans exactly three days, not day1
:- kitten(him,1).
:- not #count{ D : kitten(him,D) } = 3.

% Rottweilers not on day7 and not on any day with Himalayans
:- puppy(rot,7).
:- kitten(him,D), puppy(rot,D).

% Helper: appearances of any breed on a day
appears(B,D) :- kitten(B,D), kittenBreed(B).
appears(B,D) :- puppy(B,D), puppyBreed(B).
breed(B) :- kittenBreed(B).
breed(B) :- puppyBreed(B).

% Count breeds that appear exactly three days
count3(B) :- breed(B), #count{ D : appears(B,D) } = 3.
fourCount3 :- #count{ B : count3(B) } = 4.

% Option conditions
% A: exactly four breeds each featured on three days
option(a) :- fourCount3.

% B: Greyhounds featured on every day that Himalayans are
badB :- kitten(him,D), not puppy(grey,D).
option(b) :- not badB.

% C: Himalayans featured on every day that Greyhounds are
badC :- puppy(grey,D), not kitten(him,D).
option(c) :- not badC.

% D: Himalayans featured on every day that Rottweilers are not
badD :- day(D), not puppy(rot,D), not kitten(him,D).
option(d) :- not badD.

% E: Rottweilers featured on every day that Himalayans are not
badE :- day(D), not kitten(him,D), not puppy(rot,D).
option(e) :- not badE.

% Exactly one option must be true
:- not 1 { option(a); option(b); option(c); option(d); option(e) } 1.
:- 2 { option(a); option(b); option(c); option(d); option(e) }.

#show option/1.