% Define the domain
 day(wednesday; thursday; friday).
time(morning; afternoon).
assistant(julio; kevin; lan; nessa; olivia; rebecca).

% Define day order for Julio < Olivia constraint
day_order(wednesday, thursday).
day_order(thursday, friday).
day_order(wednesday, friday).

% Base assignment: each assistant is assigned to exactly one session
{ assigned(A, D, T) : day(D), time(T) } 1 :- assistant(A).

% Each session has exactly one assistant
:- 2 { assigned(A, D, T) : assistant(A) }, day(D), time(T).

% Constraints:
% 1. Kevin and Rebecca must lead sessions on the same day
:- assigned(kevin, D1, _), assigned(rebecca, D2, _), D1 != D2.

% 2. Lan and Olivia cannot lead sessions on the same day
:- assigned(lan, D1, _), assigned(olivia, D2, _), D1 == D2.

% 3. Nessa must lead an afternoon session
:- assigned(nessa, _, morning).

% 4. Julio's session must be on an earlier day than Olivia's
:- assigned(julio, D1, _), assigned(olivia, D2, _), not day_order(D1, D2).

% Additional condition for this specific question: Julio and Kevin both lead morning sessions
:- not assigned(julio, _, morning).
:- not assigned(kevin, _, morning).

% Define what each option means:
% Option A: Lan's session meets Wednesday morning
option_a :- assigned(lan, wednesday, morning).

% Option B: Lan's session meets Thursday afternoon
option_b :- assigned(lan, thursday, afternoon).

% Option C: Nessa's session meets Friday afternoon
option_c :- assigned(nessa, friday, afternoon).

% Option D: Olivia's session meets Thursday morning
option_d :- assigned(olivia, thursday, morning).

% Option E: Olivia's session meets Friday morning
option_e :- assigned(olivia, friday, morning).

% The correct answer is the option that is NOT possible, so we need to find which option cannot be true
% We will derive answer(X) for the option that is impossible

% If an option is possible, it cannot be the answer (since the question asks for the EXCEPT option)
% So we derive answer(X) only if X is impossible

% To determine impossibility, we use constraints to ensure that if an option is possible, it is not the answer
% We will use the following logic:
% - If option_a is possible, then answer(a) is not derived
% - If option_b is possible, then answer(b) is not derived
% - ...
% - If option_e is possible, then answer(e) is not derived
% - If none of the above are possible, then the one that is impossible is the answer

% We will derive answer(X) for the option that is impossible by ensuring it is the only one not excluded

% Exclude options that are possible
:- option_a, not answer(a).
:- option_b, not answer(b).
:- option_c, not answer(c).
:- option_d, not answer(d).
:- option_e, not answer(e).

% Derive answer(X) for the option that is impossible
% If an option is impossible, it will not appear in option_X, so we can derive answer(X) for it
answer(a) :- not option_a.
answer(b) :- not option_b.
answer(c) :- not option_c.
answer(d) :- not option_d.
answer(e) :- not option_e.

% Ensure only one answer is derived
:- answer(X), answer(Y), X != Y.

#show answer/1.