% Define domains
solo(1..5).
pianist(w; z).
type(m; t).

% Generate choices for pianist and type for each solo
{ pianist(S, P) : P = w; P = z } 1 :- solo(S).
{ type(S, T) : T = m; T = t } 1 :- solo(S).

% Constraints
% 1. The third solo is a traditional piece.
:- not type(3, t).

% 2. Exactly two of the traditional pieces are performed consecutively.
% Count consecutive traditional pairs
consecutive_pair(S) :- solo(S), S < 5, type(S, t), type(S+1, t).
:- #count{ S : consecutive_pair(S) } != 1.

% 3. In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
wayne_traditional_4 :- pianist(4, w), type(4, t).
zara_modern_4 :- pianist(4, z), type(4, m).
:- not wayne_traditional_4, not zara_modern_4.

% 4. The pianist who performs the second solo does not perform the fifth solo.
:- pianist(2, P), pianist(5, P).

% 5. No traditional piece is performed until Wayne performs at least one modern piece.
% Compute the first traditional solo
first_traditional(S) :- solo(S), type(S, t), not (solo(T), T < S, type(T, t)).
% Define if there is a modern piece by Wayne before S
has_early_modern(S) :- solo(T), T < S, pianist(T, w), type(T, m).
:- first_traditional(S), not has_early_modern(S).

% Extra condition: The pianist who performs the first solo also performs the second solo.
:- pianist(1, P1), pianist(2, P2), P1 != P2.

% Derive the answer choices.
option(a) :- pianist(1, z).
option(b) :- pianist(3, w).
option(c) :- pianist(5, z).
option(d) :- type(2, t).
option(e) :- type(4, m).

#show option/1.
#show pianist/2.
#show type/2.