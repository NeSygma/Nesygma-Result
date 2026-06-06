% People
person(alice; bob; charlie).

% Each person is either a knight or a knave
{ type(P, knight) : person(P) } 1 :- person(P).
type(P, knave) :- person(P), not type(P, knight).

% Alice says: "Bob is a knave"
% If Alice is a knight, then Bob must be a knave
:- type(alice, knight), not type(bob, knave).
% If Alice is a knave, then Bob must be a knight (since her statement is false)
:- type(alice, knave), not type(bob, knight).

% Bob says: "Alice and Charlie are of the same type"
% If Bob is a knight, then Alice and Charlie must have the same type
:- type(bob, knight), type(alice, T1), type(charlie, T2), T1 != T2.
% If Bob is a knave, then Alice and Charlie must have different types
:- type(bob, knave), type(alice, T1), type(charlie, T2), T1 == T2.

% Charlie says: "Alice is a knight"
% If Charlie is a knight, then Alice must be a knight
:- type(charlie, knight), not type(alice, knight).
% If Charlie is a knave, then Alice must be a knave (since his statement is false)
:- type(charlie, knave), type(alice, knight).

% Show the solution
#show type/2.