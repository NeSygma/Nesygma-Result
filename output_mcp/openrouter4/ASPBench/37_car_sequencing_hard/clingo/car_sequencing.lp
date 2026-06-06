%%% Domain Definitions %%%
position(1..12).

%%% Car Types and Counts %%%
car_type(a; b; c; d).

%%% Option Mapping %%%
option(1;2;3;4;5).

%%% Type-Option Mapping %%%
has_option(a, 1).
has_option(b, 3).
has_option(b, 4).
has_option(c, 2).
has_option(d, 5).

%%% Assignment: each position has exactly one car type %%%
1 { assign(P, T) : car_type(T) } 1 :- position(P).

%%% Each car type appears exactly the specified number of times %%%
:- T = a, #count { P : assign(P, a) } != 3.
:- T = b, #count { P : assign(P, b) } != 3.
:- T = c, #count { P : assign(P, c) } != 4.
:- T = d, #count { P : assign(P, d) } != 2.

%%% Derive effective options for each position %%%
% A car has an option if its type has that option
car_has_option(P, O) :- assign(P, T), has_option(T, O).

%%% Constraint 2: Hierarchical Options: Option 5 implies Option 1 for constraint purposes %%%
% Effective Option 1 means the car has Option 1 OR Option 5
eff_option(P, 1) :- car_has_option(P, 1).
eff_option(P, 1) :- car_has_option(P, 5).

%%% Constraint 3: Positional Ban: No Option 4 at position 1 or 12 %%%
:- car_has_option(1, 4).
:- car_has_option(12, 4).

%%% Constraint 4: Equipment Cooldown: Option 2 cars need 2-slot gap %%%
% If a car with Option 2 is at P, then no Option 2 at P+1 and P+2
:- car_has_option(P, 2), car_has_option(Pp1, 2), Pp1 = P + 1, position(Pp1).
:- car_has_option(P, 2), car_has_option(Pp2, 2), Pp2 = P + 2, position(Pp2).

%%% Constraint 5: Standard Capacity: at most 2 cars with effective Option 1 in any window of 4 %%%
:- position(P), Pmax = P + 3, Pmax <= 12,
   #count { Q : position(Q), Q >= P, Q <= P + 3, eff_option(Q, 1) } > 2.

%%% Constraint 6: Conditional Capacity for Option 3 %%%
% For each position P (1..12), look at window [P, P+3] if P+3 <= 12
% Determine if P is preceded by an Option 4 car at P-1 (if P >= 2)
% Actually re-reading: "If a position P is preceded by a car with EV (Option 4), then at most 1 car with Option 3 in the window [P, P+3]"
% So for window starting at P, if the car at P-1 has Option 4, then limit is 1.
% Otherwise limit is 2.

% Helper: check if position P is preceded by an Option 4 car
preceded_by_ev(P) :- position(P), P > 1, car_has_option(P - 1, 4).

% Window constraint: at most 1 if preceded by EV
:- position(P), Pmax = P + 3, Pmax <= 12, preceded_by_ev(P),
   #count { Q : position(Q), Q >= P, Q <= P + 3, car_has_option(Q, 3) } > 1.

% Window constraint: at most 2 otherwise
:- position(P), Pmax = P + 3, Pmax <= 12, not preceded_by_ev(P),
   #count { Q : position(Q), Q >= P, Q <= P + 3, car_has_option(Q, 3) } > 2.

%%% Output %%%
solution_found :- 1 = #count { P : assign(P, _) }.

#show assign/2.
#show solution_found/0.