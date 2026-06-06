% Domains
position(1..4).
historian(farley; garcia; holden; jiang).
topic(lithographs; oil_paintings; sculptures; watercolors).

% Given condition: Garcia gives the sculptures lecture
% This is a fact, not a choice - Garcia must give sculptures
1 { assignment(P, garcia, sculptures) : position(P) } 1.

% Each position has exactly one assignment
1 { assignment(P, H, T) : historian(H), topic(T) } 1 :- position(P).

% Each historian gives exactly one lecture
1 { assignment(P, H, T) : position(P), topic(T) } 1 :- historian(H).

% Each topic is covered exactly once
1 { assignment(P, H, T) : position(P), historian(H) } 1 :- topic(T).

% Constraints:
% 1. Oil paintings and watercolors must be earlier than lithographs
:- assignment(PosOil, _, oil_paintings),
   assignment(PosLith, _, lithographs),
   PosOil >= PosLith.

% Constraint: Watercolors < lithographs
:- assignment(PosWater, _, watercolors),
   assignment(PosLith, _, lithographs),
   PosWater >= PosLith.

% Constraint: Farley < oil paintings
:- assignment(PosFarley, farley, _),
   assignment(PosOil, _, oil_paintings),
   PosFarley >= PosOil.

% Constraint: Holden < Garcia
:- assignment(PosHolden, holden, _),
   assignment(PosGarcia, garcia, _),
   PosHolden >= PosGarcia.

% Constraint: Holden < Jiang
:- assignment(PosHolden, holden, _),
   assignment(PosJiang, jiang, _),
   PosHolden >= PosJiang.

% Map the options to conditions
% (A) The lithographs lecture is third
option(a) :- assignment(3, _, lithographs).

% (B) The oil paintings lecture is third
option(b) :- assignment(3, _, oil_paintings).

% (C) The sculptures lecture is first
option(c) :- assignment(1, _, sculptures).

% (D) The sculptures lecture is second
option(d) :- assignment(2, _, sculptures).

% (E) The watercolors lecture is second
option(e) :- assignment(2, _, watercolors).

#show option/1.