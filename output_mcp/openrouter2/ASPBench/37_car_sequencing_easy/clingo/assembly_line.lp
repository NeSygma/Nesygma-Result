% Domain
position(1..6).
type(a). type(b). type(c).
option(1). option(2). option(3).

% Option mapping
option_of_type(a,1). option_of_type(a,2).
option_of_type(b,3).
option_of_type(c,1).

% Choice: exactly one type per position
1 { car(Pos, T) : type(T) } 1 :- position(Pos).

% Count constraints for car types
:- #count{Pos : car(Pos, a)} != 1.
:- #count{Pos : car(Pos, b)} != 2.
:- #count{Pos : car(Pos, c)} != 3.

% Derived predicate: has_option
has_option(Pos, O) :- car(Pos, T), option_of_type(T, O).

% Option capacity constraints
% Option 1: at most 2 in any 3 consecutive cars
:- S = 1..4, #count{Pos : Pos >= S, Pos <= S+2, has_option(Pos,1)} > 2.

% Option 2: at most 1 in any 2 consecutive cars
:- S = 1..5, #count{Pos : Pos >= S, Pos <= S+1, has_option(Pos,2)} > 1.

% Option 3: at most 1 in any 2 consecutive cars
:- S = 1..5, #count{Pos : Pos >= S, Pos <= S+1, has_option(Pos,3)} > 1.

#show car/2.