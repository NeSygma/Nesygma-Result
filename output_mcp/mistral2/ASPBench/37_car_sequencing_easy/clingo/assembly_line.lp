% --- Domains ---
position(1..6).
car_type(a; b; c).
option(1; 2; 3).

% --- Car type counts ---
% Exactly 1 car of type A, 2 of type B, 3 of type C
1 { car_type(P, a) : position(P) } 1.
2 { car_type(P, b) : position(P) } 2.
3 { car_type(P, c) : position(P) } 3.

% --- Option assignments per car type ---
has_option(a, 1).  % Type A has options 1 (sunroof) and 2 (leather)
has_option(a, 2).
has_option(b, 3).  % Type B has option 3 (GPS)
has_option(c, 1).  % Type C has option 1 (sunroof)

% --- Option in car ---
option_in_car(P, O) :-
    car_type(P, T),
    has_option(T, O),
    position(P),
    option(O).

% --- Option capacity constraints ---

% Option 1: At most 2 in every 3 consecutive cars
:- option_in_car(P, 1),
   option_in_car(P+1, 1),
   option_in_car(P+2, 1),
   position(P),
   P <= 4.

% Option 2: At most 1 in every 2 consecutive cars
:- option_in_car(P, 2),
   option_in_car(P+1, 2),
   position(P),
   P <= 5.

% Option 3: At most 1 in every 2 consecutive cars
:- option_in_car(P, 3),
   option_in_car(P+1, 3),
   position(P),
   P <= 5.

% --- Show the sequence ---
#show car_type/2.