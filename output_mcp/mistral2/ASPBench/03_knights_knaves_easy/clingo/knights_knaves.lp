% Define the people
person(alice).
person(bob).
person(charlie).

% Define the possible types
type(knight).
type(knave).

% Assign types to each person (exactly one type per person)
1 { assignment(P, T) : type(T) } 1 :- person(P).

% Alice says: "Bob is a knave"
% If Alice is a knight, then Bob must be a knave.
% If Alice is a knave, then Bob must be a knight.
alice_says_truth :- assignment(alice, knight), assignment(bob, knave).
alice_says_lie   :- assignment(alice, knave), assignment(bob, knight).

% Bob says: "Alice and Charlie are of the same type"
% If Bob is a knight, then Alice and Charlie must be of the same type.
% If Bob is a knave, then Alice and Charlie must be of different types.
bob_says_truth :- assignment(bob, knight), assignment(alice, T), assignment(charlie, T).
bob_says_lie   :- assignment(bob, knave), assignment(alice, T1), assignment(charlie, T2), T1 != T2.

% Charlie says: "Alice is a knight"
% If Charlie is a knight, then Alice must be a knight.
% If Charlie is a knave, then Alice must be a knave.
charlie_says_truth :- assignment(charlie, knight), assignment(alice, knight).
charlie_says_lie   :- assignment(charlie, knave), assignment(alice, knave).

% Ensure that the statements align with the type of the speaker
:- assignment(alice, knight), not alice_says_truth.
:- assignment(alice, knave), not alice_says_lie.
:- assignment(bob, knight), not bob_says_truth.
:- assignment(bob, knave), not bob_says_lie.
:- assignment(charlie, knight), not charlie_says_truth.
:- assignment(charlie, knave), not charlie_says_lie.

% Define the output for the solution
#show assignment/2.