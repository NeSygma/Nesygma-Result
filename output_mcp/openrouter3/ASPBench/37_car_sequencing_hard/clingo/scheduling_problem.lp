% Scheduling 12 cars with hierarchical options, cooldown, and capacity constraints

% ===== DOMAIN DECLARATIONS =====
position(1..12).
car_type("A"; "B"; "C"; "D").
option(1..5).

% ===== CAR TYPE-OPTION MAPPING =====
% Type A: has Option 1 (Standard Sunroof)
has_option("A", 1).

% Type B: has Options 3, 4 (Sport Package, EV Powertrain)
has_option("B", 3).
has_option("B", 4).

% Type C: has Option 2 (Custom Paint)
has_option("C", 2).

% Type D: has Option 5 (Panoramic Sunroof)
has_option("D", 5).

% ===== ASSIGNMENT CONSTRAINTS =====
% Each position must have exactly one car type
1 { car_at(P, T) : car_type(T) } 1 :- position(P).

% Each car type must appear exactly the specified number of times
% Type A: 3 cars
count_a(N) :- N = #count{ P : position(P), car_at(P, "A") }.
:- count_a(N), N != 3.

% Type B: 3 cars  
count_b(N) :- N = #count{ P : position(P), car_at(P, "B") }.
:- count_b(N), N != 3.

% Type C: 4 cars
count_c(N) :- N = #count{ P : position(P), car_at(P, "C") }.
:- count_c(N), N != 4.

% Type D: 2 cars
count_d(N) :- N = #count{ P : position(P), car_at(P, "D") }.
:- count_d(N), N != 2.

% ===== OPTION DERIVATION =====
% A position has an option if its car type has that option
has_option_at(P, O) :- car_at(P, T), has_option(T, O).

% ===== HIERARCHICAL OPTIONS =====
% Option 5 (Panoramic Sunroof) implies Option 1 (Standard Sunroof)
has_option_at(P, 1) :- has_option_at(P, 5).

% Effective Option 1 includes both Option 1 and Option 5
effective_option1(P) :- has_option_at(P, 1).
effective_option1(P) :- has_option_at(P, 5).

% ===== POSITIONAL BAN =====
% No car with Option 4 (EV Powertrain) at position 1 or 12
:- has_option_at(1, 4).
:- has_option_at(12, 4).

% ===== EQUIPMENT COOLDOWN =====
% Cars with Option 2 (Custom Paint) must have at least 2-slot gap
% Cannot be at positions P and P+1, or P and P+2
:- has_option_at(P, 2), has_option_at(P+1, 2).
:- has_option_at(P, 2), has_option_at(P+2, 2).

% ===== STANDARD CAPACITY =====
% At most 2 cars with effective Option 1 in any window of 4 consecutive positions
:- position(P), P <= 9,
   #count{ Q : effective_option1(Q), Q >= P, Q <= P+3 } > 2.

% ===== CONDITIONAL CAPACITY FOR OPTION 3 =====
% Helper: position P has EV (Option 4)
has_ev(P) :- has_option_at(P, 4).

% Helper: position P is preceded by EV (position P-1 has EV)
preceded_by_ev(P) :- has_ev(P-1), position(P), P > 1.

% For Option 3 (Sport Package):
% If position P is preceded by EV, then at most 1 car with Option 3 in window [P, P+3]
% Otherwise, at most 2 cars with Option 3 in window [P, P+3]

% Window constraint when preceded by EV
:- position(P), P <= 9, preceded_by_ev(P),
   #count{ Q : has_option_at(Q, 3), Q >= P, Q <= P+3 } > 1.

% Window constraint when NOT preceded by EV
:- position(P), P <= 9, not preceded_by_ev(P),
   #count{ Q : has_option_at(Q, 3), Q >= P, Q <= P+3 } > 2.

% ===== SOLUTION FOUND =====
solution_found :- position(P), car_at(P, _).  % If we have a valid assignment

% ===== SHOW DIRECTIVES =====
#show solution_found/0.
#show car_at/2.
#show has_option_at/2.
#show effective_option1/1.