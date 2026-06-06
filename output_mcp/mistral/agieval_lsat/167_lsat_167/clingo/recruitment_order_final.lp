% Define the domain of people and positions
person(peters; quinn; rovero; stanton; tao; villas; white).
position(1..7).

% Base facts about fixed positions
position_four(peters).

% Choice rule: assign each position to a person
1 { assigned(Pos, Person) : person(Person) } 1 :- position(Pos).

% Each person is assigned to exactly one position
1 { assigned(Pos, Person) : position(Pos) } 1 :- person(Person).

% Constraint: Peters is in position 4
:- assigned(4, P), P != peters.

% Constraint: Villas is immediately before White
:- assigned(Pos, villas), not assigned(Pos+1, white), position(Pos+1).
:- assigned(Pos, white), not assigned(Pos-1, villas), position(Pos-1).

% Constraint: White is immediately before Quinn (specific condition for this question)
:- assigned(Pos, white), not assigned(Pos+1, quinn), position(Pos+1).
:- assigned(Pos, quinn), not assigned(Pos-1, white), position(Pos-1).

% Constraint: Quinn is earlier than Rovero
:- assigned(QPos, quinn), assigned(RPos, rovero), QPos >= RPos.

% Constraint: Stanton is not immediately before or after Tao
:- assigned(Pos, stanton), assigned(Pos+1, tao), position(Pos+1).
:- assigned(Pos, tao), assigned(Pos+1, stanton), position(Pos+1).
:- assigned(Pos, stanton), assigned(Pos-1, tao), position(Pos-1).
:- assigned(Pos, tao), assigned(Pos-1, stanton), position(Pos-1).

% Determine who is in position 6
position_six(P) :- assigned(6, P).

% Ensure only one person is in position 6
:- position_six(P1), position_six(P2), P1 != P2.

% Map the correct answer to option/1
option(a) :- position_six(quinn).
option(b) :- position_six(rovero).
option(c) :- position_six(stanton).
option(d) :- position_six(villas).
option(e) :- position_six(white).

#show option/1.