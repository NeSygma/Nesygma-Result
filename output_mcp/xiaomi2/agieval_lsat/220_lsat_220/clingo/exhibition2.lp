student(franz). student(greene). student(hidalgo). student(isaacs).
type(oil). type(watercolor).
wall(1). wall(2). wall(3). wall(4).
position(upper). position(lower).

painting(S,T) :- student(S), type(T).
slot(W,P) :- wall(W), position(P).

% Each painting assigned to exactly one slot
1 { assign(S,T,W,P) : slot(W,P) } 1 :- painting(S,T).

% Each slot gets exactly one painting
1 { assign(S,T,W,P) : painting(S,T) } 1 :- slot(W,P).

% Given facts:
% Isaacs's oil is displayed in the lower position of wall 4.
assign(isaacs, oil, 4, lower).

% Franz's oil is displayed on wall 3.
:- assign(franz, oil, W, _), W != 3.

% Isaacs's watercolor is displayed on wall 2.
:- assign(isaacs, watercolor, W, _), W != 2.

% Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
% Since Franz's oil is on wall 3, Greene's watercolor is upper on wall 3.
assign(greene, watercolor, 3, upper).

% Condition 1: No wall has only watercolors → each wall has at least one oil.
has_oil(W) :- assign(_, oil, W, _).
:- wall(W), not has_oil(W).

% Condition 2: No wall has the work of only one student → each wall has paintings from at least 2 students.
student_on_wall(S, W) :- assign(S, _, W, _).
:- wall(W), #count{S : student_on_wall(S, W)} < 2.

% Condition 3: No wall has both Franz and Isaacs.
:- assign(franz, _, W, _), assign(isaacs, _, W, _).

% Map the correct answer to option/1
option(a) :- assign(franz, watercolor, 1, _).
option(b) :- assign(greene, oil, 1, _).
option(c) :- assign(greene, watercolor, 1, _).
option(d) :- assign(hidalgo, oil, 1, _).
option(e) :- assign(hidalgo, watercolor, 1, _).

#show option/1.