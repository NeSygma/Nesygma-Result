% === Domain ===
person(alice).
person(bob).
person(charlie).

type(knight).
type(knave).

% === Each person is exactly one type ===
1 { assigned(P, T) : type(T) } 1 :- person(P).

% === Helper: check if two people are the same type ===
same_type(X, Y) :- assigned(X, T), assigned(Y, T).
diff_type(X, Y) :- assigned(X, T1), assigned(Y, T2), T1 != T2.

% === Statement truth values ===
% Alice says: "Bob is a knave"
stmt_true(alice) :- assigned(bob, knave).
stmt_false(alice) :- assigned(bob, knight).

% Bob says: "Alice and Charlie are of the same type"
stmt_true(bob) :- same_type(alice, charlie).
stmt_false(bob) :- diff_type(alice, charlie).

% Charlie says: "Alice is a knight"
stmt_true(charlie) :- assigned(alice, knight).
stmt_false(charlie) :- assigned(alice, knave).

% === Knights tell truth, knaves lie ===
:- assigned(P, knight), stmt_false(P).
:- assigned(P, knave), stmt_true(P).

% === Output ===
#show assigned/2.