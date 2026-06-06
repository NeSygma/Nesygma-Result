% Domain definitions
time(1..5).
pianist(wayne; zara).
type(modern; traditional).

% Variables for each solo
{ solo_pianist(T, P) : pianist(P) } 1 :- time(T).
{ solo_type(T, Ty) : type(Ty) } 1 :- time(T).

% Condition 1: Third solo is traditional
solo_type(3, traditional).

% Condition 2: Exactly two traditional pieces are performed consecutively
% Count consecutive traditional pairs
consecutive_traditional(T1, T2) :- T2 = T1 + 1, time(T1), time(T2), solo_type(T1, traditional), solo_type(T2, traditional).
% Exactly one such pair (since exactly two traditional pieces are consecutive)
:- N = #count{T1, T2 : consecutive_traditional(T1, T2)}, N != 1.

% Condition 3: Fourth solo: either Wayne performs traditional OR Zara performs modern
% This is an OR condition - at least one must be true
condition3_holds :- solo_pianist(4, wayne), solo_type(4, traditional).
condition3_holds :- solo_pianist(4, zara), solo_type(4, modern).
:- not condition3_holds.

% Condition 4: Pianist who performs second solo does not perform fifth solo
:- solo_pianist(2, P), solo_pianist(5, P).

% Condition 5: No traditional piece is performed until Wayne performs at least one modern piece
% This means: Before any traditional piece, Wayne must have performed at least one modern piece
% More precisely: For any time T where solo_type(T, traditional), there must exist some time T' < T where solo_pianist(T', wayne) and solo_type(T', modern)
:- solo_type(T, traditional), not exists_wayne_modern_before(T).

exists_wayne_modern_before(T) :- solo_pianist(T1, wayne), solo_type(T1, modern), T1 < T.

% Additional constraint from question: Fifth solo is traditional
solo_type(5, traditional).

% Determine which solos have completely determined pianists
% A solo has completely determined pianist if in ALL valid models, the same pianist performs it
% We need to check if for each solo position, the pianist is the same across all answer sets

% Helper: Count how many different pianists can perform each solo across all models
% We'll use a different approach: check if for each solo, only one pianist appears in any valid model
pianist_determined(T) :- time(T), #count{P : solo_pianist(T, P)} = 1.

% Count how many solos have determined pianists
num_determined(N) :- N = #count{T : pianist_determined(T)}.

% Map to answer choices
option(a) :- num_determined(1).
option(b) :- num_determined(2).
option(c) :- num_determined(3).
option(d) :- num_determined(4).
option(e) :- num_determined(5).

#show option/1.
#show solo_pianist/2.
#show solo_type/2.