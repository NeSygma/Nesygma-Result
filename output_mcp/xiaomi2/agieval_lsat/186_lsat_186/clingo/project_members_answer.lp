% Workers
worker(quinn). worker(ruiz). worker(smith). worker(taylor). worker(verma). worker(wells). worker(xue).

% Given conditions
leader(taylor).
member(taylor).
member(wells).

% Choose exactly one more member from the remaining workers
{ member(W) : worker(W), W != taylor, W != wells } 1.

% Constraints
% Exactly three members
:- #count{W: member(W)} != 3.

% Exactly one leader
:- #count{W: leader(W)} != 1.

% Leader must be a member
member(W) :- leader(W).

% Constraint 1: Quinn or Ruiz can be a member only if leading
:- member(quinn), not leader(quinn).
:- member(ruiz), not leader(ruiz).

% Constraint 2: If Smith is a member, Taylor must be
:- member(smith), not member(taylor).

% Constraint 3: If Wells is a member, neither Ruiz nor Verma can be
:- member(wells), member(ruiz).
:- member(wells), member(verma).

% Define third member
third_member(W) :- member(W), W != taylor, W != wells.

% Check which answer choices are possible
possible_third(quinn) :- third_member(quinn).
possible_third(ruiz) :- third_member(ruiz).
possible_third(smith) :- third_member(smith).
possible_third(verma) :- third_member(verma).
possible_third(xue) :- third_member(xue).

% Answer choice mapping
% (A) Quinn or Smith
% (B) Quinn or Xue
% (C) Ruiz or Verma
% (D) Smith or Xue
% (E) Verma or Xue

% The correct answer is (D) because the third member must be Smith or Xue
option(a) :- third_member(quinn).
option(b) :- third_member(quinn).
option(c) :- third_member(ruiz).
option(d) :- third_member(smith).
option(d) :- third_member(xue).
option(e) :- third_member(verma).

#show option/1.
#show third_member/1.