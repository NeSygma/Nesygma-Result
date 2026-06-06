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
before(percussionist, keyboard) :- 
    assigned(percussionist, P1), assigned(keyboard, P2), P1 < P2.
:- not before(percussionist, keyboard).

% The keyboard player performs a solo at some time after the violinist does
% and at some time before the guitarist does.
before(violinist, keyboard) :-
    assigned(violinist, P1), assigned(keyboard, P2), P1 < P2.
:- not before(violinist, keyboard).

before(keyboard, guitarist) :-
    assigned(keyboard, P1), assigned(guitarist, P2), P1 < P2.
:- not before(keyboard, guitarist).

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
% We check each option: if assigning that member to position 3 leads to unsatisfiability,
% then that member cannot be the third soloist.

% We'll use a choice to test each possibility.
% For each member M, we check if there exists a valid assignment where M is at position 3.
possible_third(M) :- member(M), assigned(M, 3).

% The answer is the member for whom possible_third is false.
% But we need to derive this from the model. Let's use a different approach:
% We'll enumerate all valid assignments and see which members appear at position 3.

% Show which members can be at position 3
#show assigned/2.
#show option/1.