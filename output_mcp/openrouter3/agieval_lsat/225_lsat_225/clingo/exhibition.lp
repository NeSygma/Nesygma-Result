% Art Exhibition Problem

% Domain declarations
student(franz). student(greene). student(hidalgo). student(isaacs).
wall(1). wall(2). wall(3). wall(4).
position(upper). position(lower).
painting_type(oil). painting_type(watercolor).

% Each student has exactly two paintings: one oil and one watercolor
% We'll represent paintings as student_type pairs
painting(Student, Type) :- student(Student), painting_type(Type).

% Each wall has exactly two paintings: one upper, one lower
% We'll represent wall assignments as wall_position_student_type
% But first, let's define the structure more clearly

% Each painting must be assigned to exactly one wall and position
% We'll use choice rules to allow all possible assignments
{ on_wall(Student, Type, Wall, Position) } :- painting(Student, Type), wall(Wall), position(Position).

% Each painting must be assigned to exactly one wall and position
1 { on_wall(Student, Type, Wall, Position) : wall(Wall), position(Position) } 1 :- painting(Student, Type).

% Each wall-position pair must have exactly one painting
1 { on_wall(Student, Type, Wall, Position) : student(Student), painting_type(Type) } 1 :- wall(Wall), position(Position).

% Constraint 1: No wall has only watercolors displayed on it
% This means each wall must have at least one oil painting
:- wall(Wall), not on_wall(_, oil, Wall, upper), not on_wall(_, oil, Wall, lower).

% Constraint 2: No wall has the work of only one student displayed on it
% This means each wall must have paintings from at least two different students
:- wall(Wall), on_wall(S1, _, Wall, _), on_wall(S2, _, Wall, _), S1 = S2, #count{S : on_wall(S, _, Wall, _)} = 1.

% Constraint 3: No wall has both a painting by Franz and a painting by Isaacs displayed on it
:- wall(Wall), on_wall(franz, _, Wall, _), on_wall(isaacs, _, Wall, _).

% Constraint 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed
% This means: Find the wall where Franz's oil is, then Greene's watercolor must be on that same wall in upper position
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

% Map the correct answer to option/1
% We need to find which one CANNOT be true
% This means we need to check if assuming each option leads to unsatisfiability

% For each option, we'll create a constraint that would make it impossible
% If adding that constraint makes the model unsatisfiable, then that option cannot be true

% Option A cannot be true if adding the constraint that A is true makes the model unsatisfiable
option(a) :- answer_a, #false.

% Option B cannot be true if adding the constraint that B is true makes the model unsatisfiable  
option(b) :- answer_b, #false.

% Option C cannot be true if adding the constraint that C is true makes the model unsatisfiable
option(c) :- answer_c, #false.

% Option D cannot be true if adding the constraint that D is true makes the model unsatisfiable
option(d) :- answer_d, #false.

% Option E cannot be true if adding the constraint that E is true makes the model unsatisfiable
option(e) :- answer_e, #false.

% Actually, we need a different approach. Let's check each option by seeing if it's possible
% We'll create separate models for each option to see which one leads to unsatisfiability

% For now, let's just show all possible assignments and then manually check
#show on_wall/4.
#show answer_a/0.
#show answer_b/0.
#show answer_c/0.
#show answer_d/0.
#show answer_e/0.