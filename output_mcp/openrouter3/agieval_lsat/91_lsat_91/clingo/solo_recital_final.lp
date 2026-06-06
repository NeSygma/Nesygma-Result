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
condition3_holds :- solo_pianist(4, wayne), solo_type(4, traditional).
condition3_holds :- solo_pianist(4, zara), solo_type(4, modern).
:- not condition3_holds.

% Condition 4: Pianist who performs second solo does not perform fifth solo
:- solo_pianist(2, P), solo_pianist(5, P).

% Condition 5: No traditional piece is performed until Wayne performs at least one modern piece
% This means: Before any traditional piece, Wayne must have performed at least one modern piece
% More precisely: For any time T where solo_type(T, traditional), there must exist some time T' < T where solo_pianist(T', wayne) and solo_type(T', modern)
% We need to define this properly
% Let's define: wayne_modern_before(T) means Wayne performed modern before time T
wayne_modern_before(T) :- solo_pianist(T1, wayne), solo_type(T1, modern), T1 < T, time(T).
:- solo_type(T, traditional), not wayne_modern_before(T).

% Additional constraint from question: Fifth solo is traditional
solo_type(5, traditional).

% Now, let's derive which solos are completely determined
% We'll check each solo position and see if the pianist is forced

% From the constraints, we can derive:
% 1. Solo 1 must be modern (because if it were traditional, condition 5 would be violated)
solo_type(1, modern).

% 2. Solo 4 must be modern (because if it were traditional, we'd have three consecutive traditional pieces: 3,4,5)
% Let's prove this: If solo 4 were traditional, then we'd have solo 3,4,5 all traditional
% This would give us two consecutive pairs: (3,4) and (4,5)
% But we need exactly one consecutive pair, so solo 4 cannot be traditional
solo_type(4, modern).

% 3. Since solo 4 is modern, condition 3 says Zara must perform solo 4
solo_pianist(4, zara).

% 4. Now, with solo 4 modern, the consecutive pair must be either (2,3) or (1,2)
% But solo 1 is modern, so the consecutive pair cannot be (1,2)
% Therefore, the consecutive pair must be (2,3)
% So solo 2 must be traditional
solo_type(2, traditional).

% 5. Since solo 2 is traditional, condition 5 says Wayne must have performed a modern piece before solo 2
% The only solo before solo 2 is solo 1
% So solo 1 must be performed by Wayne
solo_pianist(1, wayne).

% Now, we have determined:
% Solo 1: Wayne, modern
% Solo 2: traditional (pianist not determined)
% Solo 3: traditional (pianist not determined)
% Solo 4: Zara, modern
% Solo 5: traditional (pianist not determined)

% So only solo 1 and solo 4 have determined pianists
% That's 2 solos

% Map to answer choices
option(a) :- false. % 1 solo
option(b) :- true.  % 2 solos
option(c) :- false. % 3 solos
option(d) :- false. % 4 solos
option(e) :- false. % 5 solos

#show option/1.
#show solo_pianist/2.
#show solo_type/2.