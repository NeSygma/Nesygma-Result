% --- Domain ---
person(alice).
person(bob).
person(charlie).

% --- Choice Rule: Each person is either a knight or a knave ---
{ is_knight(P) } :- person(P).
is_knave(P) :- person(P), not is_knight(P).

% --- Logical Constraints based on statements ---
% Alice says: "Bob is a knave"
% If Alice is a knight, Bob is a knave. If Alice is a knave, Bob is a knight.
is_knight(alice) :- is_knave(bob).
is_knave(alice) :- is_knight(bob).

% Bob says: "Alice and Charlie are of the same type"
% If Bob is a knight, Alice and Charlie are the same.
% If Bob is a knave, Alice and Charlie are different.
is_knight(bob) :- is_knight(alice), is_knight(charlie).
is_knight(bob) :- is_knave(alice), is_knave(charlie).
is_knave(bob) :- is_knight(alice), is_knave(charlie).
is_knave(bob) :- is_knave(alice), is_knight(charlie).

% Charlie says: "Alice is a knight"
% If Charlie is a knight, Alice is a knight.
% If Charlie is a knave, Alice is a knave.
is_knight(charlie) :- is_knight(alice).
is_knave(charlie) :- is_knave(alice).

% --- Output Mapping ---
type(alice, "knight") :- is_knight(alice).
type(alice, "knave") :- is_knave(alice).
type(bob, "knight") :- is_knight(bob).
type(bob, "knave") :- is_knave(bob).
type(charlie, "knight") :- is_knight(charlie).
type(charlie, "knave") :- is_knave(charlie).

#show type/2.