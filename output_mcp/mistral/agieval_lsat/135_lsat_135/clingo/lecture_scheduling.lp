% Define the lecture positions
position(1..5).

% Define bird types
bird(oystercatchers; petrels; rails; sandpipers; terns).

% Define locations
location(gladwyn; howard).

% Assign a location to each position
% Exactly 3 in Gladwyn Hall, so exactly 2 in Howard Auditorium
1 { location_at(P, gladwyn) : position(P) } 3.
1 { location_at(P, howard) : position(P) } 2.

% Constraints:
% 1. First lecture is in Gladwyn Hall
location_at(1, gladwyn).

% 2. Fourth lecture is in Howard Auditorium
location_at(4, howard).

% Assign a bird type to each position
{ bird_at(P, B) : bird(B) } 1 :- position(P).

% 4. Sandpipers is in Howard Auditorium and earlier than oystercatchers
:- bird_at(P, sandpipers), location_at(P, gladwyn).
:- bird_at(P1, sandpipers), bird_at(P2, oystercatchers), P1 >= P2.

% 5. Terns is earlier than petrels, and petrels is in Gladwyn Hall
:- bird_at(P1, terns), bird_at(P2, petrels), P1 >= P2.
:- bird_at(P, petrels), location_at(P, howard).

% Check which options are possible
% Option A: positions 1 and 2 are both in Gladwyn Hall
possible_a :- location_at(1, gladwyn), location_at(2, gladwyn).

% Option B: positions 2 and 3 are both in Howard Auditorium
possible_b :- location_at(2, howard), location_at(3, howard).

% Option C: positions 2 and 5 are both in Gladwyn Hall
possible_c :- location_at(2, gladwyn), location_at(5, gladwyn).

% Option D: positions 3 and 4 are both in Howard Auditorium
possible_d :- location_at(3, howard), location_at(4, howard).

% Option E: positions 3 and 5 are both in Gladwyn Hall
possible_e :- location_at(3, gladwyn), location_at(5, gladwyn).

% The answer is the option that must be false (i.e., the one that is NOT possible in any model)
% We derive must_be_false(X) if possible_X is not satisfied in any model
% To do this, we assume that if possible_X is not derived in any model, it must be false
% We use a constraint to ensure that at least one option must be false

% Derive must_be_false(X) if possible_X is not derived
must_be_false(a) :- not possible_a.
must_be_false(b) :- not possible_b.
must_be_false(c) :- not possible_c.
must_be_false(d) :- not possible_d.
must_be_false(e) :- not possible_e.

% Map the correct answer to option/1 (MANDATORY)
% The correct answer is the option that must be false
option(a) :- must_be_false(a), not must_be_false(b), not must_be_false(c), not must_be_false(d), not must_be_false(e).
option(b) :- must_be_false(b), not must_be_false(a), not must_be_false(c), not must_be_false(d), not must_be_false(e).
option(c) :- must_be_false(c), not must_be_false(a), not must_be_false(b), not must_be_false(d), not must_be_false(e).
option(d) :- must_be_false(d), not must_be_false(a), not must_be_false(b), not must_be_false(c), not must_be_false(e).
option(e) :- must_be_false(e), not must_be_false(a), not must_be_false(b), not must_be_false(c), not must_be_false(d).

#show option/1.
#show possible_a/0.
#show possible_b/0.
#show possible_c/0.
#show possible_d/0.
#show possible_e/0.
#show must_be_false/1.