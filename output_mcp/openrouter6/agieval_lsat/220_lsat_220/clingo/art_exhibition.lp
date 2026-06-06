% Art Exhibition Logic Puzzle

% Domains
student(franz). student(greene). student(hidalgo). student(isaacs).
type(oil). type(watercolor).
wall(1..4).
position(upper). position(lower).

% Each painting is placed exactly once
% Choice rule: for each student and type, choose exactly one wall and position
{ placed(Student, Type, Wall, Position) : wall(Wall), position(Position) } 1 :- student(Student), type(Type).

% Each wall has exactly one painting in upper and one in lower position
% Use explicit variables to avoid unsafe variables
1 { placed(S, T, Wall, upper) : student(S), type(T) } 1 :- wall(Wall).
1 { placed(S, T, Wall, lower) : student(S), type(T) } 1 :- wall(Wall).

% Constraint 1: No wall has only watercolors (each wall must have at least one oil)
:- wall(Wall), not placed(_, oil, Wall, _).

% Constraint 2: No wall has work of only one student (two paintings on a wall must be from different students)
:- placed(S, _, Wall, upper), placed(S, _, Wall, lower).

% Constraint 3: No wall has both Franz and Isaacs
:- placed(franz, _, Wall, _), placed(isaacs, _, Wall, _).

% Constraint 4: Greene's watercolor is in the upper position of the wall where Franz's oil is displayed
placed(greene, watercolor, W, upper) :- placed(franz, oil, W, _).

% Constraint 5: Isaacs's oil is in the lower position of wall 4
placed(isaacs, oil, 4, lower).

% Additional assumptions for the question
% Isaacs's watercolor is on wall 2 (position unknown)
:- placed(isaacs, watercolor, W, _), W != 2.
% Franz's oil is on wall 3 (position unknown)
:- placed(franz, oil, W, _), W != 3.

% Helper predicate to check what's on wall 1
on_wall1(Student, Type) :- placed(Student, Type, 1, _).

% Check each option
% (A) Franz's watercolor
option_a :- on_wall1(franz, watercolor).
% (B) Greene's oil
option_b :- on_wall1(greene, oil).
% (C) Greene's watercolor
option_c :- on_wall1(greene, watercolor).
% (D) Hidalgo's oil
option_d :- on_wall1(hidalgo, oil).
% (E) Hidalgo's watercolor
option_e :- on_wall1(hidalgo, watercolor).

% Map the correct answer to option/1 (MANDATORY)
% We need to determine which option is forced (true in all valid models)
% Since we expect a unique solution, we can check which option is true
option(a) :- option_a, not option_b, not option_c, not option_d, not option_e.
option(b) :- option_b, not option_a, not option_c, not option_d, not option_e.
option(c) :- option_c, not option_a, not option_b, not option_d, not option_e.
option(d) :- option_d, not option_a, not option_b, not option_c, not option_e.
option(e) :- option_e, not option_a, not option_b, not option_c, not option_d.

% Show the option
#show option/1.

% For debugging, show all placements
#show placed/4.