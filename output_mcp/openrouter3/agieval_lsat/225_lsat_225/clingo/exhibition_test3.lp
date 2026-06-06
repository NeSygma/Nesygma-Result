% Art Exhibition Problem - Testing each option individually

% Domain declarations
student(franz). student(greene). student(hidalgo). student(isaacs).
wall(1). wall(2). wall(3). wall(4).
position(upper). position(lower).
painting_type(oil). painting_type(watercolor).

% Each student has exactly two paintings: one oil and one watercolor
painting(Student, Type) :- student(Student), painting_type(Type).

% Each painting must be assigned to exactly one wall and position
1 { on_wall(Student, Type, Wall, Position) : wall(Wall), position(Position) } 1 :- painting(Student, Type).

% Each wall-position pair must have exactly one painting
1 { on_wall(Student, Type, Wall, Position) : student(Student), painting_type(Type) } 1 :- wall(Wall), position(Position).

% Constraint 1: No wall has only watercolors displayed on it
:- wall(Wall), not on_wall(_, oil, Wall, upper), not on_wall(_, oil, Wall, lower).

% Constraint 2: No wall has the work of only one student displayed on it
:- wall(Wall), #count{S : on_wall(S, _, Wall, _)} < 2.

% Constraint 3: No wall has both a painting by Franz and a painting by Isaacs displayed on it
:- wall(Wall), on_wall(franz, _, Wall, _), on_wall(isaacs, _, Wall, _).

% Constraint 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed
:- on_wall(franz, oil, Wall, _), not on_wall(greene, watercolor, Wall, upper).

% Constraint 5: Isaacs's oil is displayed in the lower position of wall 4
:- not on_wall(isaacs, oil, 4, lower).

% Helper predicates for answer choices
% A: Franz's watercolor is displayed on the same wall as Greene's oil
answer_a :- on_wall(franz, watercolor, Wall, _), on_wall(greene, oil, Wall, _).

% B: Franz's watercolor is displayed on the same wall as Hidalgo's oil
answer_b :- on_wall(franz, watercolor, Wall, _), on_wall(hidalgo, oil, Wall, _).

% C: Greene's oil is displayed in an upper position
answer_c :- on_wall(greene, oil, _, upper).

% D: Hidalgo's watercolor is displayed in a lower position
answer_d :- on_wall(hidalgo, watercolor, _, lower).

% E: Isaacs's watercolor is displayed on the same wall as Hidalgo's oil
answer_e :- on_wall(isaacs, watercolor, Wall, _), on_wall(hidalgo, oil, Wall, _).

% Test each option by adding a constraint that would make it true
% If the model becomes unsatisfiable, then that option cannot be true

% Test A: Add constraint that A must be true
test_a :- answer_a.
:- not test_a.  % Force A to be true

% Show result for A
#show test_a/0.

% For the final answer, we need to check which option cannot be true
% Let's create separate tests for each option

% Actually, let's use a different approach: check each option in isolation
% We'll create separate models for each option

% For now, let's just show the base model
#show on_wall/4.
#show answer_a/0.
#show answer_b/0.
#show answer_c/0.
#show answer_d/0.
#show answer_e/0.