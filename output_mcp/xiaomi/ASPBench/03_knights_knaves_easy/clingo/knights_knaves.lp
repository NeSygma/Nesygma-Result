% Domain
person(alice).
person(bob).
person(charlie).

% Each person is exactly one type
1 { type(P, knight); type(P, knave) } 1 :- person(P).

% Helper predicates
is_knight(P) :- type(P, knight).
is_knave(P) :- type(P, knave).

% Statement truth conditions
% Alice says: "Bob is a knave"
statement_true(alice) :- is_knave(bob).
statement_false(alice) :- is_knight(bob).

% Bob says: "Alice and Charlie are of the same type"
statement_true(bob) :- is_knight(alice), is_knight(charlie).
statement_true(bob) :- is_knave(alice), is_knave(charlie).
statement_false(bob) :- is_knight(alice), is_knave(charlie).
statement_false(bob) :- is_knave(alice), is_knight(charlie).

% Charlie says: "Alice is a knight"
statement_true(charlie) :- is_knight(alice).
statement_false(charlie) :- is_knave(alice).

% Knights tell the truth - their statements must be true
:- type(P, knight), statement_false(P).

% Knaves lie - their statements must be false
:- type(P, knave), statement_true(P).

% Output
#show type/2.