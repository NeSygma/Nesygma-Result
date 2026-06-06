% --- Domain Definitions ---
car_type(a; b; c).
option(1; 2; 3).
position(1..6).

% --- Instance Data ---
has_option(a, 1).
has_option(a, 2).
has_option(b, 3).
has_option(c, 1).

count(a, 1).
count(b, 2).
count(c, 3).

% --- Assignment ---
% Each position must have exactly one car type
{ assigned(Type, Pos) : car_type(Type) } = 1 :- position(Pos).

% --- Constraints ---
% 1. Respect car type counts
:- car_type(T), count(T, N), #count { Pos : assigned(T, Pos) } != N.

% Helper: Does car at position P have option O?
has_opt(Pos, Opt) :- assigned(Type, Pos), has_option(Type, Opt).

% 2. Option 1 (sunroof): at most 2 in every 3 consecutive cars
:- position(P), P <= 4, #count { P1 : P <= P1, P1 < P+3, has_opt(P1, 1) } > 2.

% 3. Option 2 (leather): at most 1 in every 2 consecutive cars
:- position(P), P <= 5, #count { P1 : P <= P1, P1 < P+2, has_opt(P1, 2) } > 1.

% 4. Option 3 (GPS): at most 1 in every 2 consecutive cars
:- position(P), P <= 5, #count { P1 : P <= P1, P1 < P+2, has_opt(P1, 3) } > 1.

% --- Output ---
#show assigned/2.