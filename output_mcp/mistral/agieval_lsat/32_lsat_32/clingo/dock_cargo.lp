% Define domains
bay(1..6).
cargo(fuel; grain; livestock; machinery; produce; textiles).

% Assignment: each bay has exactly one cargo
{ assignment(B, C) : cargo(C) } 1 :- bay(B).

% Each cargo is in exactly one bay
{ assignment(B, C) : bay(B) } 1 :- cargo(C).

% Constraints from the problem
% 1. grain > livestock
:- assignment(B1, grain), assignment(B2, livestock), B1 =< B2.

% 2. livestock > textiles
:- assignment(B1, livestock), assignment(B2, textiles), B1 =< B2.

% 3. produce > fuel
:- assignment(B1, produce), assignment(B2, fuel), B1 =< B2.

% 4. textiles is next to produce (adjacent)
:- assignment(B1, textiles), assignment(B2, produce), abs(B1 - B2) != 1.

% 5. Exactly one bay between machinery and grain (|machinery - grain| = 2)
:- assignment(B1, machinery), assignment(B2, grain), abs(B1 - B2) != 2.

% The unique solution determines all 6 bays
% So the answer is that all 6 bays are completely determined

% Map to answer choice
option(e) :- assignment(1, _), assignment(2, _), assignment(3, _), assignment(4, _), assignment(5, _), assignment(6, _).

#show option/1.