% Base facts about the accomplices and positions
person("Peters").
person("Quinn").
person("Rovero").
person("Stanton").
person("Tao").
person("Villas").
person("White").

position(1..7).

% Tao was recruited second (given)
recruited("Tao", 2).

% Peters was recruited fourth (given)
recruited("Peters", 4).

% Villas was recruited immediately before White
1 { recruited("Villas", V) : position(V) } 1.
1 { recruited("White", W) : position(W) } 1.
:- recruited("Villas", V), recruited("White", W), W != V + 1.

% Quinn was recruited earlier than Rovero
1 { recruited("Quinn", Q) : position(Q) } 1.
1 { recruited("Rovero", R) : position(R) } 1.
:- recruited("Quinn", Q), recruited("Rovero", R), Q >= R.

% Stanton was recruited neither immediately before nor immediately after Tao
:- recruited("Stanton", 1), recruited("Tao", 2).
:- recruited("Stanton", 3), recruited("Tao", 2).

% Ensure all positions are filled with distinct people
1 { recruited(P, Pos) : person(P) } 1 :- position(Pos).
:- person(P1), person(P2), P1 != P2, recruited(P1, Pos), recruited(P2, Pos).

% Check answer choices
% (A) Quinn was recruited third
option(a) :- recruited("Quinn", 3).

% (B) Rovero was recruited fifth
option(b) :- recruited("Rovero", 5).

% (C) Stanton was recruited sixth
option(c) :- recruited("Stanton", 6).

% (D) Villas was recruited sixth
option(d) :- recruited("Villas", 6).

% (E) White was recruited third
option(e) :- recruited("White", 3).

#show option/1.