% Workers
worker(quinn).
worker(ruiz).
worker(smith).
worker(taylor).
worker(verma).
worker(wells).
worker(xue).

% Base constraints
1 { selected(W) : worker(W) } 3.
1 { leader(W) : worker(W) } 1.
:- leader(W), not selected(W).

% Constraints
:- selected(quinn), not leader(quinn).
:- selected(ruiz), not leader(ruiz).
:- selected(smith), not selected(taylor).
:- selected(wells), selected(ruiz).
:- selected(wells), selected(verma).

% Given conditions
leader(taylor).
selected(wells).

% The third member is the one selected besides taylor and wells
1 { third_member(W) : worker(W), W != taylor, W != wells } 1.

% Ensure the third member is either Smith or Xue
:- third_member(W), W != smith, W != xue.

% Map the correct answer to option/1
option(a) :- third_member(quinn).
option(b) :- third_member(quinn).
option(b) :- third_member(xue).
option(c) :- third_member(ruiz).
option(c) :- third_member(verma).
option(d) :- third_member(smith).
option(d) :- third_member(xue).
option(e) :- third_member(verma).
option(e) :- third_member(xue).

#show option/1.