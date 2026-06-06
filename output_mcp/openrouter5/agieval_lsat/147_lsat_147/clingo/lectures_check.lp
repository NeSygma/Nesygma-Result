% Domain: historians and topics
historian(farley; garcia; holden; jiang).
topic(lithographs; oil_paintings; sculptures; watercolors).

% Each historian gives exactly one lecture (on a different topic)
1 { gives(H, T) : topic(T) } 1 :- historian(H).
% Each topic is assigned to exactly one historian
1 { gives(H, T) : historian(H) } 1 :- topic(T).

% Ordering: we have positions 1..4
position(1..4).
% Each lecture is at a unique position
1 { at_position(T, P) : position(P) } 1 :- topic(T).
1 { at_position(T, P) : topic(T) } 1 :- position(P).

% Constraints:

% The oil paintings lecture and the watercolors lecture must both be earlier than the lithographs lecture.
:- at_position(oil_paintings, P1), at_position(lithographs, P2), P1 >= P2.
:- at_position(watercolors, P1), at_position(lithographs, P2), P1 >= P2.

% Farley's lecture must be earlier than the oil paintings lecture.
:- gives(farley, T), at_position(T, P1), at_position(oil_paintings, P2), P1 >= P2.

% Holden's lecture must be earlier than both Garcia's lecture and Jiang's lecture.
:- gives(holden, T1), gives(garcia, T2), at_position(T1, P1), at_position(T2, P2), P1 >= P2.
:- gives(holden, T1), gives(jiang, T2), at_position(T1, P1), at_position(T2, P2), P1 >= P2.

% Check each option individually by forcing it and seeing if UNSAT.

% Option A: Farley gives lithographs
:- not gives(farley, lithographs).