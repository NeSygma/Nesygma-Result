% Art Exhibition Problem - Testing each option

% Domain declarations
student(franz). student(greene). student(hidalgo). student(isaacs).
wall(1). wall(2). wall(3). wall(4).
position(upper). position(lower).
painting_type(oil). painting_type(watercolor).

% Each student has exactly two paintings: one oil and one watercolor
painting(Student, Type) :- student(Student), painting_type(Type).

% Each painting must be assigned to exactly one wall and position
{ on_wall(Student, Type, Wall, Position) } :- painting(Student, Type), wall(Wall), position(Position).

% Each painting must be assigned to exactly one wall and position
1 { on_wall(Student, Type, Wall, Position) : wall(Wall), position(Position) } 1 :- painting(Student, Type).

% Each wall-position pair must have exactly one painting
1 { on_wall(Student, Type, Wall, Position) : student(Student), painting_type(Type) } 1 :- wall(Wall), position(Position).

% Constraint 1: No wall has only watercolors displayed on it
:- wall(Wall), not on_wall(_, oil, Wall, upper), not on_wall(_, oil, Wall, lower).

% Constraint 2: No wall has the work of only one student displayed on it
% This means each wall must have paintings from at least two different students
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

% Test each option by adding constraints that would make them true
% If adding that constraint makes the model unsatisfiable, then that option cannot be true

% Test option A: Assume A is true and see if model remains satisfiable
test_a :- answer_a.
% If test_a is false (i.e., adding answer_a makes model unsatisfiable), then A cannot be true

% Test option B: Assume B is true and see if model remains satisfiable
test_b :- answer_b.

% Test option C: Assume C is true and see if model remains satisfiable
test_c :- answer_c.

% Test option D: Assume D is true and see if model remains satisfiable
test_d :- answer_d.

% Test option E: Assume E is true and see if model remains satisfiable
test_e :- answer_e.

% Map the correct answer to option/1
% We need to find which option CANNOT be true
% This means we need to check which option, when assumed true, makes the model unsatisfiable

% For each option, we'll create a separate test
% If the test fails (i.e., the option cannot be true), then that option is the answer

% Actually, let's use a different approach: check each option individually
% We'll create separate models for each option

% For now, let's just show the base model and then manually check
#show on_wall/4.
#show answer_a/0.
#show answer_b/0.
#show answer_c/0.
#show answer_d/0.
#show answer_e/0.