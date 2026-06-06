% Members
member(guitarist; keyboard_player; percussionist; saxophonist; trumpeter; violinist).

% Positions 1-6
position(1..6).

% Each member gets exactly one position (solo order)
1 { assigned(M, P) : position(P) } 1 :- member(M).

% Each position has exactly one member
1 { assigned(M, P) : member(M) } 1 :- position(P).

% Rule 1: The guitarist does not perform the fourth solo.
:- assigned(guitarist, 4).

% Rule 2: The percussionist performs a solo at some time before the keyboard player does.
before(M1, M2) :- assigned(M1, P1), assigned(M2, P2), P1 < P2.
:- not before(percussionist, keyboard_player).

% Rule 3: The keyboard player performs a solo at some time after the violinist does AND at some time before the guitarist does.
:- not before(violinist, keyboard_player).
:- not before(keyboard_player, guitarist).

% Rule 4: The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both.
% After percussionist XOR after trumpeter.
% after_perc = percussionist < saxophonist
% after_trump = trumpeter < saxophonist
% exactly one of these is true
after_perc(P) :- before(percussionist, X), P = X.
after_trump(P) :- before(trumpeter, X), P = X.

% Wait, let me redo this more carefully.

% Define: sax is after perc?
sax_after_perc :- before(percussionist, saxophonist).
% Define: sax is after trumpeter?
sax_after_trump :- before(trumpeter, saxophonist).

% Exactly one of these holds.
:- not sax_after_perc, not sax_after_trump.
:- sax_after_perc, sax_after_trump.

% Additional condition from the question: percussionist performs a solo at some time before the saxophonist does.
% i.e., percussionist < saxophonist.
:- not before(percussionist, saxophonist).

% Show assignments
#show assigned/2.
#show before/2.