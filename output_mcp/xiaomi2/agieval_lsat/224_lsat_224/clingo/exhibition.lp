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

% Combine oil and watercolor into a general painting predicate.
painting(S, oil, W, P) :- oil(S, W, P).
painting(S, watercolor, W, P) :- watercolor(S, W, P).

% Each wall has exactly one painting in upper and one in lower position.
:- wall(W), position(P), #count{ S, T : painting(S, T, W, P) } != 1.

% Constraint 1: No wall has only watercolors (each wall must have at least one oil).
oil_on_wall(W) :- oil(S, W, _).
:- wall(W), not oil_on_wall(W).

% Constraint 2: No wall has the work of only one student.
student_on_wall(W, S) :- painting(S, _, W, _).
:- wall(W), #count{ S : student_on_wall(W, S) } = 1.

% Constraint 3: No wall has both Franz and Isaacs.
:- wall(W), painting(franz, _, W, _), painting(isaacs, _, W, _).

% Constraint 4: Greene's watercolor is in the upper position of the wall where Franz's oil is.
:- oil(franz, W, _), not watercolor(greene, W, upper).

% Evaluate each option: which could be true?
% (A) Both of Franz's paintings and both of Greene's paintings are displayed in lower positions.
check_a :- oil(franz, _, lower), watercolor(franz, _, lower),
           oil(greene, _, lower), watercolor(greene, _, lower).

% (B) Both of Franz's paintings and both of Greene's paintings are displayed in upper positions.
check_b :- oil(franz, _, upper), watercolor(franz, _, upper),
           oil(greene, _, upper), watercolor(greene, _, upper).

% (C) Both of Franz's paintings and both of Hidalgo's paintings are displayed in upper positions.
check_c :- oil(franz, _, upper), watercolor(franz, _, upper),
           oil(hidalgo, _, upper), watercolor(hidalgo, _, upper).

% (D) Both of Greene's paintings and both of Hidalgo's paintings are displayed in lower positions.
check_d :- oil(greene, _, lower), watercolor(greene, _, lower),
           oil(hidalgo, _, lower), watercolor(hidalgo, _, lower).

% (E) Both of Greene's paintings and both of Hidalgo's paintings are displayed in upper positions.
check_e :- oil(greene, _, upper), watercolor(greene, _, upper),
           oil(hidalgo, _, upper), watercolor(hidalgo, _, upper).

% Map the correct answer to option/1
option(a) :- check_a.
option(b) :- check_b.
option(c) :- check_c.
option(d) :- check_d.
option(e) :- check_e.

#show option/1.