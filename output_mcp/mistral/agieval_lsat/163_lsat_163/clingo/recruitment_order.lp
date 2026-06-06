% Define the accomplices
accomplice(peters).
accomplice(quinn).
accomplice(rovero).
accomplice(stanton).
accomplice(tao).
accomplice(villas).
accomplice(white).

% Define positions
position(1..7).

% Assign each position to exactly one accomplice
1 { assigned(Pos, Acc) : accomplice(Acc) } 1 :- position(Pos).

% Each accomplice is assigned to exactly one position
1 { assigned(Pos, Acc) : position(Pos) } 1 :- accomplice(Acc).

% Peters was recruited fourth
assigned(4, peters).

% Villas was recruited immediately before White
:- assigned(Pos, white), assigned(Pos+1, villas), position(Pos), position(Pos+1).
:- assigned(Pos, Acc1), assigned(Pos+1, Acc2), Acc1 != villas, Acc2 = white, position(Pos), position(Pos+1).

% Quinn was recruited earlier than Rovero
:- assigned(PosQ, quinn), assigned(PosR, rovero), PosQ >= PosR.

% Stanton was recruited neither immediately before nor immediately after Tao
:- assigned(PosS, stanton), assigned(PosT, tao), abs(PosS - PosT) = 1.
:- assigned(PosS, tao), assigned(PosT, stanton), abs(PosS - PosT) = 1.

% Define the order of the middle five positions (2-6) for each option
% Option A: Quinn, Stanton, Peters, Tao, Villas
answer_a :- 
    assigned(2, quinn),
    assigned(3, stanton),
    assigned(4, peters),
    assigned(5, tao),
    assigned(6, villas).

% Option B: Quinn, Stanton, Peters, Tao, White
answer_b :- 
    assigned(2, quinn),
    assigned(3, stanton),
    assigned(4, peters),
    assigned(5, tao),
    assigned(6, white).

% Option C: Villas, White, Peters, Quinn, Stanton
answer_c :- 
    assigned(2, villas),
    assigned(3, white),
    assigned(4, peters),
    assigned(5, quinn),
    assigned(6, stanton).

% Option D: Villas, White, Peters, Rovero, Stanton
answer_d :- 
    assigned(2, villas),
    assigned(3, white),
    assigned(4, peters),
    assigned(5, rovero),
    assigned(6, stanton).

% Option E: Villas, White, Quinn, Rovero, Stanton
answer_e :- 
    assigned(2, villas),
    assigned(3, white),
    assigned(4, peters),
    assigned(5, rovero),
    assigned(6, stanton).

% Ensure only one option is correct
:- answer_a, answer_b.
:- answer_a, answer_c.
:- answer_a, answer_d.
:- answer_a, answer_e.
:- answer_b, answer_c.
:- answer_b, answer_d.
:- answer_b, answer_e.
:- answer_c, answer_d.
:- answer_c, answer_e.
:- answer_d, answer_e.

% Map the correct answer to option/1
option(a) :- answer_a.
option(b) :- answer_b.
option(c) :- answer_c.
option(d) :- answer_d.
option(e) :- answer_e.

#show option/1.