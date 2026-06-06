% Assembly Line Scheduling Problem

% Domain declarations
car_type(a; b; c).
option(1; 2; 3).
position(1..6).

% Car type to options mapping
has_option(a, 1). has_option(a, 2).  % Type A has sunroof and leather
has_option(b, 3).                     % Type B has GPS
has_option(c, 1).                     % Type C has sunroof

% Exactly one car type per position
1 { car_at_position(T, P) : car_type(T) } 1 :- position(P).

% Type count constraints
count_a(N) :- N = #count{P : car_at_position(a, P)}.
count_b(N) :- N = #count{P : car_at_position(b, P)}.
count_c(N) :- N = #count{P : car_at_position(c, P)}.
:- count_a(N), N != 1.  % Exactly 1 type A
:- count_b(N), N != 2.  % Exactly 2 type B
:- count_c(N), N != 3.  % Exactly 3 type C

% Option presence at each position
option_at_position(O, P) :- car_at_position(T, P), has_option(T, O).

% Option 1 constraint: at most 2 in any 3 consecutive cars
:- position(P), P <= 4, 
   N = #count{Q : option_at_position(1, Q), Q >= P, Q <= P+2}, N > 2.

% Option 2 constraint: at most 1 in any 2 consecutive cars
:- position(P), P <= 5,
   N = #count{Q : option_at_position(2, Q), Q >= P, Q <= P+1}, N > 1.

% Option 3 constraint: at most 1 in any 2 consecutive cars
:- position(P), P <= 5,
   N = #count{Q : option_at_position(3, Q), Q >= P, Q <= P+1}, N > 1.

% Show the sequence
#show car_at_position/2.
#show option_at_position/2.