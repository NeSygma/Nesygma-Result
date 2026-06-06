% Knights and Knaves problem
% People: Alice, Bob, Charlie

person(alice).
person(bob).
person(charlie).

% Each person is exactly one type: knight or knave
1 { type(P, "knight") ; type(P, "knave") } 1 :- person(P).

% Helper predicates for readability
knight(P) :- type(P, "knight").
knave(P) :- type(P, "knave").

% Statements content
% Alice says: "Bob is a knave"
alice_says_bob_knave :- type(bob, "knave").

% Bob says: "Alice and Charlie are of the same type"
bob_says_same_type :- type(alice, "knight"), type(charlie, "knight").
bob_says_same_type :- type(alice, "knave"), type(charlie, "knave").

% Charlie says: "Alice is a knight"
charlie_says_alice_knight :- type(alice, "knight").

% Truth conditions: knights tell truth, knaves lie
% Alice
:- knight(alice), not alice_says_bob_knave.
:- knave(alice), alice_says_bob_knave.

% Bob
:- knight(bob), not bob_says_same_type.
:- knave(bob), bob_says_same_type.

% Charlie
:- knight(charlie), not charlie_says_alice_knight.
:- knave(charlie), charlie_says_alice_knight.

% Show the assignment
#show type/2.
#show knight/1.
#show knave/1.