% Domain definitions
time(1..5).
pianist(wayne; zara).
type(modern; traditional).

% Variables for each solo
{ solo_pianist(T, P) : pianist(P) } 1 :- time(T).
{ solo_type(T, Tp) : type(Tp) } 1 :- time(T).

% Constraint 1: Third solo is traditional
:- solo_type(3, modern).

% Constraint 2: Exactly two traditional pieces are performed consecutively
% Count consecutive traditional pairs
consecutive_pair(T) :- time(T), T < 5, solo_type(T, traditional), solo_type(T+1, traditional).
:- #count{T : consecutive_pair(T)} != 1.

% Constraint 3: Fourth solo: either Wayne performs traditional OR Zara performs modern
:- solo_type(4, traditional), solo_pianist(4, zara).
:- solo_type(4, modern), solo_pianist(4, wayne).

% Constraint 4: Pianist of second solo ≠ pianist of fifth solo
:- solo_pianist(2, P), solo_pianist(5, P).

% Constraint 5: No traditional piece until Wayne performs at least one modern piece
% For each position T that is traditional, Wayne must have performed modern before T
:- time(T), solo_type(T, traditional), not wayne_modern_before(T).

% Helper: Wayne performed modern before position T
wayne_modern_before(T) :- time(T), time(M), M < T, solo_pianist(M, wayne), solo_type(M, modern).

% Define which positions are traditional for answer checking
traditional_position(T) :- time(T), solo_type(T, traditional).

% Answer choices mapping - check if the set of traditional positions matches exactly
% A: first, third, and fourth are traditional
option(a) :- 
    traditional_position(1), traditional_position(3), traditional_position(4),
    not traditional_position(2), not traditional_position(5).

% B: second, third, and fourth are traditional
option(b) :- 
    traditional_position(2), traditional_position(3), traditional_position(4),
    not traditional_position(1), not traditional_position(5).

% C: third and fourth are traditional
option(c) :- 
    traditional_position(3), traditional_position(4),
    not traditional_position(1), not traditional_position(2), not traditional_position(5).

% D: third and fifth are traditional
option(d) :- 
    traditional_position(3), traditional_position(5),
    not traditional_position(1), not traditional_position(2), not traditional_position(4).

% E: fourth and fifth are traditional
option(e) :- 
    traditional_position(4), traditional_position(5),
    not traditional_position(1), not traditional_position(2), not traditional_position(3).

#show option/1.