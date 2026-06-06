% Domain and basic facts
position(1..12).
car_type(a; b; c; d).

% Car type counts
count(a, 3).
count(b, 3).
count(c, 4).
count(d, 2).

% Option definitions
option(1..5).

% Car type to option mapping
has_option(a, 1).
has_option(b, 3).
has_option(b, 4).
has_option(c, 2).
has_option(d, 5).

% Assignment: each position gets exactly one car type
1 { assigned(P, T) : car_type(T) } 1 :- position(P).

% Each car type appears exactly the required number of times
:- count(T, N), #count { P : assigned(P, T) } != N.

% Derive which options are present at each position
has_option_at(P, O) :- assigned(P, T), has_option(T, O).

% Effective Option 1: sunroofs (including panoramic sunroof which implies standard)
effective_option1(P) :- has_option_at(P, 1).
effective_option1(P) :- has_option_at(P, 5).

% Effective Option 3 and 4 for conditional constraints
effective_option3(P) :- has_option_at(P, 3).
effective_option4(P) :- has_option_at(P, 4).

% Constraint 3: Positional ban - EV (Option 4) cannot be at position 1 or 12
:- assigned(1, T), has_option(T, 4).
:- assigned(12, T), has_option(T, 4).

% Constraint 4: Equipment cooldown - Option 2 (Custom Paint) must have at least 2-slot gap
% Cannot be at P and P+1
:- assigned(P, T), has_option(T, 2), assigned(P+1, T2), has_option(T2, 2).
% Cannot be at P and P+2
:- assigned(P, T), has_option(T, 2), assigned(P+2, T2), has_option(T2, 2).

% Constraint 5: Standard capacity - at most 2 effective Option 1 (sunroofs) in any window of 4 consecutive positions
:- position(P), P <= 9, 3 { effective_option1(P) ; effective_option1(P+1) ; effective_option1(P+2) ; effective_option1(P+3) } 2.

% Constraint 6: Conditional capacity for Option 3 (Sport Package)
% If position P is preceded by a car with EV (Option 4), then at most 1 Option 3 in window [P, P+3]
% Otherwise, at most 2 Option 3 in window [P, P+3]

% Case 1: P >= 2 and P <= 9 (so P-1 exists and window [P, P+3] fits)
:- position(P), P >= 2, P <= 9, effective_option4(P-1),
   2 { effective_option3(Q) : Q = P..P+3 } 1.

:- position(P), P >= 2, P <= 9, not effective_option4(P-1),
   3 { effective_option3(Q) : Q = P..P+3 } 2.

% Case 2: P = 1 (no predecessor, use "otherwise" case)
:- position(1),
   3 { effective_option3(Q) : Q = 1..4 } 2.

% Solution indicator
solution_found :- assigned(_, _).

% Show the solution
#show assigned/2.
#show solution_found.