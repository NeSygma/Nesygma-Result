% Knights and Knaves Puzzle

% Domain: People
person(alice).
person(bob).
person(charlie).

% Choice rule for types - each person is exactly one type
1 { type(X, "knight") ; type(X, "knave") } 1 :- person(X).

% Statement definitions
% Alice's statement: "Bob is a knave"
statement(alice, bob_is_knave).
% Bob's statement: "Alice and Charlie are of the same type"
statement(bob, alice_charlie_same_type).
% Charlie's statement: "Alice is a knight"
statement(charlie, alice_is_knight).

% Truth values of statements (derived from types)
% Alice's statement is true iff Bob is a knave
truth_value(bob_is_knave, true) :- type(bob, "knave").
truth_value(bob_is_knave, false) :- type(bob, "knight").

% Bob's statement is true iff Alice and Charlie have same type
truth_value(alice_charlie_same_type, true) :- type(alice, "knight"), type(charlie, "knight").
truth_value(alice_charlie_same_type, true) :- type(alice, "knave"), type(charlie, "knave").
truth_value(alice_charlie_same_type, false) :- type(alice, "knight"), type(charlie, "knave").
truth_value(alice_charlie_same_type, false) :- type(alice, "knave"), type(charlie, "knight").

% Charlie's statement is true iff Alice is a knight
truth_value(alice_is_knight, true) :- type(alice, "knight").
truth_value(alice_is_knight, false) :- type(alice, "knave").

% Knights tell truth: if person is knight, their statement must be true
:- type(X, "knight"), statement(X, S), truth_value(S, false).

% Knaves lie: if person is knave, their statement must be false
:- type(X, "knave"), statement(X, S), truth_value(S, true).

% Show the solution
#show type/2.