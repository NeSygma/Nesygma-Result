% Domains
position(1..4).
historian(farley; garcia; holden; jiang).
topic(lithographs; oil_paintings; sculptures; watercolors).

% Base assignment: each position has exactly one historian and one topic
1 { assignment(P, H, T) : historian(H), topic(T) } 1 :- position(P).

% Each historian gives exactly one lecture
1 { assignment(P, H, T) : position(P), topic(T) } 1 :- historian(H).

% Each topic is covered exactly once
1 { assignment(P, H, T) : position(P), historian(H) } 1 :- topic(T).

% Given condition: Garcia gives the sculptures lecture
assignment(P, garcia, sculptures) :- position(P).

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

% Define the answer choices as mutually exclusive possibilities
% We will check each option individually to ensure uniqueness

% (A) The lithographs lecture is third
answer(a) :- assignment(3, _, lithographs).

% (B) The oil paintings lecture is third
answer(b) :- assignment(3, _, oil_paintings).

% (C) The sculptures lecture is first
answer(c) :- assignment(1, _, sculptures).

% (D) The sculptures lecture is second
answer(d) :- assignment(2, _, sculptures).

% (E) The watercolors lecture is second
answer(e) :- assignment(2, _, watercolors).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- answer(a).
option(b) :- answer(b).
option(c) :- answer(c).
option(d) :- answer(d).
option(e) :- answer(e).

#show option/1.