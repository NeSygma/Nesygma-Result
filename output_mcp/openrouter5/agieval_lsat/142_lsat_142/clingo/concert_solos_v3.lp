% Domain: positions 1 through 6
position(1..6).

% Band members
member(guitarist).
member(keyboard).
member(percussionist).
member(saxophonist).
member(trumpeter).
member(violinist).

% Each member performs exactly one solo at a unique position
1 { assigned(M, P) : position(P) } 1 :- member(M).
1 { assigned(M, P) : member(M) } 1 :- position(P).

% The guitarist does not perform the fourth solo.
:- assigned(guitarist, 4).

% The percussionist performs a solo at some time before the keyboard player does.
:- assigned(percussionist, P1), assigned(keyboard, P2), P1 >= P2.

% The keyboard player performs a solo at some time after the violinist does
:- assigned(violinist, P1), assigned(keyboard, P2), P1 >= P2.

% and at some time before the guitarist does.
:- assigned(keyboard, P1), assigned(guitarist, P2), P1 >= P2.

% The saxophonist performs a solo at some time after either the percussionist does
% or the trumpeter does, but not both.
% "after either A or B but not both" means:
% (sax after perc) XOR (sax after trump)
after_perc_sax :- assigned(percussionist, P1), assigned(saxophonist, P2), P1 < P2.
after_trump_sax :- assigned(trumpeter, P1), assigned(saxophonist, P2), P1 < P2.

% Exactly one of these must hold
:- not after_perc_sax, not after_trump_sax.
:- after_perc_sax, after_trump_sax.

% Now determine which member CANNOT perform the third solo.
% We'll check each option by testing if assigning that member to position 3
% leads to a contradiction.

% For each candidate, we check if there's a valid assignment with them at position 3.
% We'll use a brute-force enumeration approach: generate all valid assignments
% and see which members appear at position 3.

% First, let's just collect all valid assignments and see who can be at position 3.
% We'll use a helper predicate.

can_be_third(M) :- assigned(M, 3).

% Show all assignments and who can be third
#show assigned/2.
#show can_be_third/1.