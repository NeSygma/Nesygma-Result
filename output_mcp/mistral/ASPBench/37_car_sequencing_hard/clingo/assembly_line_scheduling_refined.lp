% Assembly Line Scheduling Problem (Refined)

% --- DOMAINS ---
position(1..12).
car_type(a;b;c;d).

% Car type counts
count(a,3).
count(b,3).
count(c,4).
count(d,2).

% Car type to options mapping
car_type_options(a,1).
car_type_options(b,3).
car_type_options(b,4).
car_type_options(c,2).
car_type_options(d,5).

% Hierarchical options: Option 5 implies Option 1
option_implies(5,1).

% --- BASE CHOICE: Assign car types to positions ---
% Exactly one car type per position
1 { assigned(P, T) : car_type(T) } 1 :- position(P).

% Each car type appears exactly its specified count
:- count(T, N), #count { P : assigned(P, T) } != N.

% --- DERIVE OPTIONS FROM CAR TYPES ---
has_option(P, O) :- assigned(P, T), car_type_options(T, O).

% Hierarchical options: Option 5 implies Option 1
has_option(P, 1) :- has_option(P, 5).

% --- CONSTRAINT 3: Positional ban for Option 4 (EV Powertrain) ---
% No car with Option 4 at position 1 or position 12
:- assigned(1, T), has_option(1, 4).
:- assigned(12, T), has_option(12, 4).

% --- CONSTRAINT 4: Equipment cooldown for Option 2 (Custom Paint) ---
% Cars with Option 2 must have at least a 2-slot gap between them
% Cannot be at positions P and P+1
:- assigned(P, T), has_option(P, 2), assigned(P+1, T2), has_option(P+1, 2).
% Cannot be at positions P and P+2
:- assigned(P, T), has_option(P, 2), assigned(P+2, T2), has_option(P+2, 2).

% --- CONSTRAINT 5: Standard capacity for effective Option 1 (sunroofs) ---
% At most 2 cars with effective Option 1 in any window of 4 consecutive positions
% Effective Option 1 = has_option(P,1)

% Define effective Option 1 positions
effective_option1(P) :- has_option(P, 1).

% Check all windows of 4 consecutive positions
:- position(P), P <= 9,
   #count { Q : effective_option1(Q), Q >= P, Q <= P+3 } > 2.

% --- CONSTRAINT 6: Conditional capacity for Option 3 (Sport Package) ---
% For each position P, check the window [P, P+3]
% If P is preceded by EV (Option 4 at P-1), then at most 1 Option 3 in [P, P+3]
% Otherwise, at most 2 Option 3 in [P, P+3]

% Helper: preceded by EV at position P-1
preceded_by_ev(P) :- position(P), P > 1, has_option(P-1, 4).

% Count Option 3 in window [P, P+3]
:- position(P), P <= 9,
   preceded_by_ev(P),
   #count { Q : has_option(Q, 3), Q >= P, Q <= P+3 } > 1.

:- position(P), P <= 9,
   not preceded_by_ev(P),
   #count { Q : has_option(Q, 3), Q >= P, Q <= P+3 } > 2.

% --- SHOW: Indicate a solution was found ---
solution_found.
#show solution_found/0.
#show assigned/2.
#show has_option/2.