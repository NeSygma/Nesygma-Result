% Domain declarations
solo(1..5).
pianist_name(w).
pianist_name(z).
piece_type(m). % modern
piece_type(t). % traditional

% Choice rules for assignments
{ pianist(S, P) } :- solo(S), pianist_name(P).
{ type(S, T) } :- solo(S), piece_type(T).

% Each solo has exactly one pianist and one type
1 { pianist(S, P) : pianist_name(P) } 1 :- solo(S).
1 { type(S, T) : piece_type(T) } 1 :- solo(S).

% Constraint 1: Third solo is traditional
:- not type(3, t).

% Constraint 2: Exactly two traditional pieces are performed consecutively
% Count consecutive traditional pairs
consecutive_traditional(S1, S2) :- S2 = S1 + 1, type(S1, t), type(S2, t).
:- N = #count{ S1 : consecutive_traditional(S1, _) }, N != 2.

% Constraint 3: Fourth solo: Wayne performs traditional OR Zara performs modern
% This is an OR condition - at least one must be true
fourth_condition :- pianist(4, w), type(4, t).
fourth_condition :- pianist(4, z), type(4, m).
:- not fourth_condition.

% Constraint 4: Pianist who performs second solo does not perform fifth solo
:- pianist(2, P), pianist(5, P).

% Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece
% Find Wayne's first modern piece
wayne_first_modern(S) :- pianist(S, w), type(S, m), not (pianist(S2, w), type(S2, m), S2 < S).
% All traditional pieces must come after Wayne's first modern piece
:- type(S, t), wayne_first_modern(S_first), S <= S_first.

% Additional premise for the question: Pianist who performs first solo also performs second solo
premise :- pianist(1, P), pianist(2, P).
:- not premise. % This is the condition we're analyzing

% Answer choices mapping
% (A) Zara performs first solo
option(a) :- pianist(1, z).

% (B) Wayne performs third solo
option(b) :- pianist(3, w).

% (C) Zara performs fifth solo
option(c) :- pianist(5, z).

% (D) Second solo is traditional
option(d) :- type(2, t).

% (E) Fourth solo is modern
option(e) :- type(4, m).

#show option/1.