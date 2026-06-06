% Scientists
scientist(f; g; h; k; l; m; p; q; r).

% Types
botanist(f; g; h).
chemist(k; l; m).
zoologist(p; q; r).

% Selection: each scientist is either selected or not
{ selected(X) } :- scientist(X).

% At least one of each type
:- not selected(X) : botanist(X).
:- not selected(X) : chemist(X).
:- not selected(X) : zoologist(X).

% If more than one botanist selected, then at most one zoologist selected
more_than_one_botanist :- #count{ B : botanist(B), selected(B) } > 1.
:- more_than_one_botanist, #count{ Z : zoologist(Z), selected(Z) } > 1.

% F and K cannot both be selected
:- selected(f), selected(k).

% K and M cannot both be selected
:- selected(k), selected(m).

% If M is selected, both P and R must be selected
:- selected(m), not selected(p).
:- selected(m), not selected(r).

% Exactly 5 panelists
:- #count{ X : selected(X) } != 5.

% Condition: both G and H are selected
:- not selected(g).
:- not selected(h).

% Now test each option: which pair MUST include at least one?
% We check if it's possible to have a valid panel with NEITHER of the two.
% If impossible, then the option is required.

% Option A: F or else K
possible_neither_f_k :- not selected(f), not selected(k).

% Option B: F or else M
possible_neither_f_m :- not selected(f), not selected(m).

% Option C: K or else M
possible_neither_k_m :- not selected(k), not selected(m).

% Option D: M or else Q
possible_neither_m_q :- not selected(m), not selected(q).

% Option E: P or else Q
possible_neither_p_q :- not selected(p), not selected(q).

% Determine which options are required (i.e., having neither is impossible)
required(a) :- not possible_neither_f_k.
required(b) :- not possible_neither_f_m.
required(c) :- not possible_neither_k_m.
required(d) :- not possible_neither_m_q.
required(e) :- not possible_neither_p_q.

% The correct answer is the one that is required
option(a) :- required(a).
option(b) :- required(b).
option(c) :- required(c).
option(d) :- required(d).
option(e) :- required(e).

#show option/1.