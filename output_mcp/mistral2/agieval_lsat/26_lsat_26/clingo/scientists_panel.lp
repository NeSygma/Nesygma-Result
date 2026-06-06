% Define the scientists and their types
botanist("F"). botanist("G"). botanist("H").
chemist("K"). chemist("L"). chemist("M").
zoologist("P"). zoologist("Q"). zoologist("R").

scientist(S) :- botanist(S).
scientist(S) :- chemist(S).
scientist(S) :- zoologist(S).

% Define the panel size
panel_size(5).

% Selection of scientists
1 { selected(S) : scientist(S) } 5.

% At least one scientist of each type
:- not 1 { selected(S) : botanist(S) } 1.
:- not 1 { selected(S) : chemist(S) } 1.
:- not 1 { selected(S) : zoologist(S) } 1.

% If more than one botanist is selected, then at most one zoologist is selected
:- 2 { selected(S) : botanist(S) }, 2 { selected(S) : zoologist(S) }.

% F and K cannot both be selected
:- selected("F"), selected("K").

% K and M cannot both be selected
:- selected("K"), selected("M").

% If M is selected, both P and R must be selected
:- selected("M"), not selected("P").
:- selected("M"), not selected("R").

% M is the only chemist selected
selected("M") :- chemist(S), selected(S).
:- chemist(S), selected(S), S != "M".

% Define the answer choices
% (A) F and G are both selected
answer_a :- selected("F"), selected("G").

% (B) G and H are both selected
answer_b :- selected("G"), selected("H").

% (C) H and P are both selected
answer_c :- selected("H"), selected("P").

% (D) F, G, and H are all selected
answer_d :- selected("F"), selected("G"), selected("H").

% (E) P, Q, and R are all selected
answer_e :- selected("P"), selected("Q"), selected("R").

% Map the correct answer to option/1
option(a) :- answer_a, not answer_b, not answer_c, not answer_d, not answer_e.
option(b) :- answer_b, not answer_a, not answer_c, not answer_d, not answer_e.
option(c) :- answer_c, not answer_a, not answer_b, not answer_d, not answer_e.
option(d) :- answer_d, not answer_a, not answer_b, not answer_c, not answer_e.
option(e) :- answer_e, not answer_a, not answer_b, not answer_c, not answer_d.

#show option/1.