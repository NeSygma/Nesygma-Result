% Define the scientists and their types
botanist(f). botanist(g). botanist(h).
chemist(k). chemist(l). chemist(m).
zoologist(p). zoologist(q). zoologist(r).

scientist(X) :- botanist(X).
scientist(X) :- chemist(X).
scientist(X) :- zoologist(X).

% Define the types of scientists
type(X, botanist) :- botanist(X).
type(X, chemist) :- chemist(X).
type(X, zoologist) :- zoologist(X).

% Panel size: 5 scientists
panel_size(5).

% Select exactly 5 scientists
1 { selected(X) : scientist(X) } 5.

% At least one scientist of each type
:- not 1 { selected(X) : type(X, botanist) } 1.
:- not 1 { selected(X) : type(X, chemist) } 1.
:- not 1 { selected(X) : type(X, zoologist) } 1.

% If more than one botanist is selected, then at most one zoologist is selected
:- 2 { selected(X) : type(X, botanist) }, 2 { selected(X) : type(X, zoologist) }.

% F and K cannot both be selected
:- selected(f), selected(k).

% K and M cannot both be selected
:- selected(k), selected(m).

% If M is selected, both P and R must be selected
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% Base constraints for the multiple-choice question
% If both G and H are among the selected scientists
both_g_and_h_selected :- selected(g), selected(h).

% Define the conditions for each option
% (A) F or else K
option(a) :- both_g_and_h_selected, selected(f).
option(a) :- both_g_and_h_selected, not selected(f), selected(k).

% (B) F or else M
option(b) :- both_g_and_h_selected, selected(f).
option(b) :- both_g_and_h_selected, not selected(f), selected(m).

% (C) K or else M
option(c) :- both_g_and_h_selected, selected(k).
option(c) :- both_g_and_h_selected, not selected(k), selected(m).

% (D) M or else Q
option(d) :- both_g_and_h_selected, selected(m).
option(d) :- both_g_and_h_selected, not selected(m), selected(q).

% (E) P or else Q
option(e) :- both_g_and_h_selected, selected(p).
option(e) :- both_g_and_h_selected, not selected(p), selected(q).

% Ensure that only one option is selected
:- option(A), option(B), A != B.
:- option(A), option(C), A != C.
:- option(A), option(D), A != D.
:- option(A), option(E), A != E.
:- option(B), option(C), B != C.
:- option(B), option(D), B != D.
:- option(B), option(E), B != E.
:- option(C), option(D), C != D.
:- option(C), option(E), C != E.
:- option(D), option(E), D != E.

#show option/1.
#show both_g_and_h_selected/0.
#show selected/1.