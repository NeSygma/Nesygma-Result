% Domains
student(franz). student(greene). student(hidalgo). student(isaacs).
wall(1). wall(2). wall(3). wall(4).
position(upper). position(lower).

% Each student has exactly one oil painting placed somewhere.
1 { oil(S, W, P) : wall(W), position(P) } 1 :- student(S).

% Each student has exactly one watercolor painting placed somewhere.
1 { watercolor(S, W, P) : wall(W), position(P) } 1 :- student(S).

% Isaacs's oil is fixed on wall 4, lower position.
oil(isaacs, 4, lower).

% Combine oil and watercolor into a general painting predicate for counting.
painting(S, oil, W, P) :- oil(S, W, P).
painting(S, watercolor, W, P) :- watercolor(S, W, P).

% Each wall has exactly one painting in upper and one in lower position.
:- wall(W), position(P), #count{ S, T : painting(S, T, W, P) } != 1.

% Constraint 1: No wall has only watercolors.
oil_on_wall(W) :- oil(S, W, _).
:- wall(W), not oil_on_wall(W).

% Constraint 2: No wall has the work of only one student.
student_on_wall(W, S) :- painting(S, _, W, _).
:- wall(W), #count{ S : student_on_wall(W, S) } = 1.

% Constraint 3: No wall has both Franz and Isaacs.
:- wall(W), painting(franz, _, W, _), painting(isaacs, _, W, _).

% Constraint 4: Greene's watercolor is in the upper position of the wall where Franz's oil is.
:- oil(franz, W, _), not watercolor(greene, W, upper).

% Define conditions for each option.
condition_a :- oil(franz, W1, lower), watercolor(franz, W2, lower), oil(greene, W3, lower), watercolor(greene, W4, lower).
condition_b :- oil(franz, W1, upper), watercolor(franz, W2, upper), oil(greene, W3, upper), watercolor(greene, W4, upper).
condition_c :- oil(franz, W1, upper), watercolor(franz, W2, upper), oil(hidalgo, W3, upper), watercolor(hidalgo, W4, upper).
condition_d :- oil(greene, W1, lower), watercolor(greene, W2, lower), oil(hidalgo, W3, lower), watercolor(hidalgo, W4, lower).
condition_e :- oil(greene, W1, upper), watercolor(greene, W2, upper), oil(hidalgo, W3, upper), watercolor(hidalgo, W4, upper).

% Choose one option to be true.
{ option(a); option(b); option(c); option(d); option(e) }.

% If an option is selected, its condition must hold.
:- option(a), not condition_a.
:- option(b), not condition_b.
:- option(c), not condition_c.
:- option(d), not condition_d.
:- option(e), not condition_e.

#show option/1.