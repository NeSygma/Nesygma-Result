% Domains
position(1..6).
car_type(a;b;c).
option(1;2;3).

% Option assignments per car type
% Type A: options 1 (sunroof) and 2 (leather)
has_option(a,1). has_option(a,2).
% Type B: option 3 (GPS)
has_option(b,3).
% Type C: option 1 (sunroof)
has_option(c,1).

% Assign exactly one car type to each position
1 { car_type(P, T) : car_type(T) } 1 :- position(P).

% Enforce car type counts (1×A, 2×B, 3×C)
% At most 1 car of type A
:- 2 { car_type(P, a) : position(P) }.
% At most 2 cars of type B
:- 3 { car_type(P, b) : position(P) }.
% At most 3 cars of type C
:- 4 { car_type(P, c) : position(P) }.

% Define which positions have which options
% Note: has_option_at(P, O) is true if the car at position P has option O
has_option_at(P, O) :- car_type(P, T), has_option(T, O), position(P), option(O).

% Option 1 constraint: at most 2 in every 3 consecutive cars
% Define all 3-position windows
window3(P;P+1;P+2) :- position(P), P <= 4.

% Count option 1 in each window
count_option1_in_window(P, C) :-
    window3(P;P+1;P+2),
    C = #count { Q : has_option_at(Q, 1), Q >= P, Q <= P+2 }.

% Constrain count to be at most 2
:- count_option1_in_window(P, C), C > 2.

% Option 2 constraint: at most 1 in every 2 consecutive cars
% Define all 2-position windows
window2(P;P+1) :- position(P), P <= 5.

% Count option 2 in each window
count_option2_in_window(P, C) :-
    window2(P;P+1),
    C = #count { Q : has_option_at(Q, 2), Q >= P, Q <= P+1 }.

% Constrain count to be at most 1
:- count_option2_in_window(P, C), C > 1.

% Option 3 constraint: at most 1 in every 2 consecutive cars
% Count option 3 in each window
count_option3_in_window(P, C) :-
    window2(P;P+1),
    C = #count { Q : has_option_at(Q, 3), Q >= P, Q <= P+1 }.

% Constrain count to be at most 1
:- count_option3_in_window(P, C), C > 1.

% Show the solution
#show car_type/2.