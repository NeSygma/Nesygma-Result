person(alice; bob; charlie).

% Each person is either knight or knave
{ knight(P) } :- person(P).
knave(P) :- person(P), not knight(P).

% Alice's statement: "Bob is a knave"
% If Alice is knight, Bob is knave (not knight)
:- knight(alice), knight(bob).
% If Alice is knave, Bob is knight
:- knave(alice), not knight(bob).

% Bob's statement: "Alice and Charlie are of the same type"
% If Bob is knight, Alice and Charlie are same type
:- knight(bob), knight(alice), not knight(charlie).
:- knight(bob), not knight(alice), knight(charlie).
% If Bob is knave, Alice and Charlie are different types
:- knave(bob), knight(alice), knight(charlie).
:- knave(bob), not knight(alice), not knight(charlie).

% Charlie's statement: "Alice is a knight"
% If Charlie is knight, Alice is knight
:- knight(charlie), not knight(alice).
% If Charlie is knave, Alice is knave
:- knave(charlie), knight(alice).

#show knight/1.
#show knave/1.