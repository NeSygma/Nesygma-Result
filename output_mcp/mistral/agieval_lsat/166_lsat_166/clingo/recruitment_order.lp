% Define the seven accomplices
person(peters).
person(quinn).
person(rovero).
person(stanton).
person(tao).
person(villas).
person(white).

% Define positions 1 through 7
position(1..7).

% Each position has exactly one person recruited
1 { recruited(Person, Pos) : person(Person) } 1 :- position(Pos).

% Each person is recruited at exactly one position
1 { recruited(Person, Pos) : position(Pos) } 1 :- person(Person).

% Stanton was recruited neither immediately before nor immediately after Tao
:- recruited(stanton, Pos1), recruited(tao, Pos2), Pos2 = Pos1 + 1.
:- recruited(stanton, Pos1), recruited(tao, Pos2), Pos2 = Pos1 - 1.

% Quinn was recruited earlier than Rovero
:- recruited(quinn, PosQ), recruited(rovero, PosR), PosQ >= PosR.

% Villas was recruited immediately before White
:- recruited(villas, PosV), recruited(white, PosW), PosW != PosV + 1.

% Peters was recruited fourth
:- not recruited(peters, 4).

% Additional conditions from the question:
% White was recruited earlier than Rovero
:- recruited(white, PosW), recruited(rovero, PosR), PosW >= PosR.

% Rovero was recruited earlier than Tao
:- recruited(rovero, PosR), recruited(tao, PosT), PosR >= PosT.


% Map the correct answer to option/1
% We need to check which option COULD be true
% Since we're looking for "could be true", we check consistency

% Option A: Quinn was recruited first
option(a) :- recruited(quinn, 1).

% Option B: Rovero was recruited third
option(b) :- recruited(rovero, 3).

% Option C: Stanton was recruited second
option(c) :- recruited(stanton, 2).

% Option D: Tao was recruited sixth
option(d) :- recruited(tao, 6).

% Option E: Villas was recruited sixth
option(e) :- recruited(villas, 6).

#show option/1.