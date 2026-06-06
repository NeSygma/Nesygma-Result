% Define the band members
member(guitarist).
member(keyboard).
member(percussionist).
member(saxophonist).
member(trumpeter).
member(violinist).

% Define positions (solos are numbered 1 through 6)
position(1..6).

% Each member performs exactly one solo
1 { solo(M, P) : position(P) } 1 :- member(M).

% Each position has exactly one performer
1 { solo(M, P) : member(M) } 1 :- position(P).

% Constraint: The guitarist does not perform the fourth solo
:- solo(guitarist, 4).

% Constraint: The percussionist performs before the keyboard player
:- solo(percussionist, P1), solo(keyboard, P2), P1 >= P2.

% Constraint: The keyboard player performs after the violinist and before the guitarist
:- solo(keyboard, Pk), solo(violinist, Pv), Pk =< Pv.
:- solo(keyboard, Pk), solo(guitarist, Pg), Pk >= Pg.

% Define when saxophonist is after percussionist
sax_after_percussion :- solo(saxophonist, Ps), solo(percussionist, Pp), Ps > Pp.

% Define when saxophonist is after trumpeter
sax_after_trumpeter :- solo(saxophonist, Ps), solo(trumpeter, Pt), Ps > Pt.

% Constraint: Saxophonist performs after exactly one of percussionist or trumpeter
:- sax_after_percussion, sax_after_trumpeter.
:- not sax_after_percussion, not sax_after_trumpeter.

% Define the conditions for each answer choice being true

% (A) The keyboard player performs the first solo
keyboard_first :- solo(keyboard, 1).

% (B) The guitarist performs the second solo
guitarist_second :- solo(guitarist, 2).

% (C) The guitarist performs a solo at some time before the saxophonist does
guitarist_before_sax :- solo(guitarist, Pg), solo(saxophonist, Ps), Pg < Ps.

% (D) The guitarist performs a solo at some time before the percussionist does
guitarist_before_percussion :- solo(guitarist, Pg), solo(percussionist, Pp), Pg < Pp.

% (E) The keyboard player performs a solo at some time before the saxophonist does
keyboard_before_sax :- solo(keyboard, Pk), solo(saxophonist, Ps), Pk < Ps.

% Map the correct answer to option/1
% The question asks: "Each of the following must be false EXCEPT:"
% This means we need to find which option CAN be true (is not necessarily false)
% We will check which of these conditions can be true in a valid model

option(a) :- keyboard_first.
option(b) :- guitarist_second.
option(c) :- guitarist_before_sax.
option(d) :- guitarist_before_percussion.
option(e) :- keyboard_before_sax.

#show option/1.