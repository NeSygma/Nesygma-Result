% Define workers
worker(quinn).
worker(ruiz).
worker(smith).
worker(taylor).
worker(verma).
worker(wells).
worker(xue).

% Base constraints:
% Exactly 3 workers are selected
3 { selected(W) : worker(W) } 3.

% Exactly 1 leader among selected workers
1 { leader(W) : selected(W) } 1.

% Constraints:
% Quinn or Ruiz can be a project member only if leading the project
:- selected(quinn), not leader(quinn).
:- selected(ruiz), not leader(ruiz).

% If Smith is a project member, Taylor must also be
:- selected(smith), not selected(taylor).

% If Wells is a project member, neither Ruiz nor Verma can be
:- selected(wells), selected(ruiz).
:- selected(wells), selected(verma).

% Define the conditions for each option
% Option A: Neither Quinn nor Smith is selected
condition_a :- not selected(quinn), not selected(smith).

% Option B: Neither Quinn nor Taylor is selected
condition_b :- not selected(quinn), not selected(taylor).

% Option C: Neither Quinn nor Xue is selected
condition_c :- not selected(quinn), not selected(xue).

% Option D: Neither Ruiz nor Wells is selected
condition_d :- not selected(ruiz), not selected(wells).

% Option E: Neither Ruiz nor Verma is selected
condition_e :- not selected(ruiz), not selected(verma).

% Check if the condition leads to a unique solution
% We do this by ensuring that only one condition is satisfied in the model
unique_condition :- condition_a, not condition_b, not condition_c, not condition_d, not condition_e.
unique_condition :- condition_b, not condition_a, not condition_c, not condition_d, not condition_e.
unique_condition :- condition_c, not condition_a, not condition_b, not condition_d, not condition_e.
unique_condition :- condition_d, not condition_a, not condition_b, not condition_c, not condition_e.
unique_condition :- condition_e, not condition_a, not condition_b, not condition_c, not condition_d.

% Map the correct answer to option/1 only if the condition is unique
option(a) :- condition_a, unique_condition.
option(b) :- condition_b, unique_condition.
option(c) :- condition_c, unique_condition.
option(d) :- condition_d, unique_condition.
option(e) :- condition_e, unique_condition.

% Ensure only one option is selected
:- option(X), option(Y), X != Y.

#show option/1.
#show selected/1.
#show leader/1.