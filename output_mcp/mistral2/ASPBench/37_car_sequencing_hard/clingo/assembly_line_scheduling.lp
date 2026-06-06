% --- DOMAINS ---
position(1..12).
car_type("A"; "B"; "C"; "D").
option(1..5).

% --- CAR TYPE-OPTION MAPPING ---
car_type_option("A", 1).
car_type_option("B", 3).
car_type_option("B", 4).
car_type_option("C", 2).
car_type_option("D", 5).

% --- ASSIGNMENT ---
{ assigned(Pos, Type) : car_type(Type) } = 1 :- position(Pos).

% --- DERIVED OPTIONS ---
% has_option(Pos, Opt) is true if the car at Pos has Opt

has_option(Pos, Opt) :-
    assigned(Pos, Type),
    car_type_option(Type, Opt).

% Hierarchical Options: Option 5 implies Option 1
has_option(Pos, 1) :- has_option(Pos, 5).

% --- COUNT CONSTRAINTS ---
count_car_type(Type, N) :-
    N = #count{ Pos : assigned(Pos, Type) },
    car_type(Type).

:- count_car_type("A", N), N != 3.
:- count_car_type("B", N), N != 3.
:- count_car_type("C", N), N != 4.
:- count_car_type("D", N), N != 2.

% --- POSITIONAL BAN ---
:- assigned(1, Type) : has_option(1, 4).
:- assigned(12, Type) : has_option(12, 4).

% --- EQUIPMENT COOLDOWN (Option 2: Custom Paint) ---
% No two Option 2 cars within 2 slots
:- has_option(P, 2), has_option(P+1, 2).
:- has_option(P, 2), has_option(P+2, 2).

% --- STANDARD CAPACITY (Option 1: Sunroofs) ---
% At most 2 cars with Option 1 in any window of 4 consecutive positions
:- position(P),
   P <= 9,
   #count{ Q : Q = P..P+3, has_option(Q, 1) } > 2.

% --- CONDITIONAL CAPACITY (Option 3: Sport Package) ---
% Helper: preceded_by_ev(P) is true if position P-1 has Option 4
preceded_by_ev(P) :- position(P), P > 1, has_option(P-1, 4).

% If preceded by EV, at most 1 Option 3 in [P, P+3]
:- position(P),
   P <= 9,
   preceded_by_ev(P),
   #count{ Q : Q = P..P+3, has_option(Q, 3) } > 1.

% Otherwise, at most 2 Option 3 in [P, P+3]
:- position(P),
   P <= 9,
   not preceded_by_ev(P),
   #count{ Q : Q = P..P+3, has_option(Q, 3) } > 2.

% --- OUTPUT ---
#show sequence(Pos, Type, Opts) :-
    assigned(Pos, Type),
    car_type_option(Type, Opt),
    Opts = Opt.