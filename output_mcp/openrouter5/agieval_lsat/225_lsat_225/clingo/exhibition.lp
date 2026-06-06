%%% DOMAIN DEFINITIONS %%%

% Students
student(franz; greene; hidalgo; isaacs).

% Walls
wall(1;2;3;4).

% Positions
position(upper; lower).

% Mediums
medium(oil; watercolor).

%%% CHOICE RULES: Assign each student's two paintings to walls and positions %%%

% Each student has exactly one oil painting and one watercolor painting.
% We assign each student's oil to a wall and position, and each student's watercolor to a wall and position.

% Student's oil: assigned to exactly one wall and one position
{ student_placement(Student, oil, Wall, Pos) : wall(Wall), position(Pos) } 1 :- student(Student).

% Student's watercolor: assigned to exactly one wall and one position
{ student_placement(Student, watercolor, Wall, Pos) : wall(Wall), position(Pos) } 1 :- student(Student).

%%% CONSTRAINTS %%%

% Exactly two paintings on each wall (one upper, one lower)
% Upper position on each wall: exactly one painting
:- wall(W), not 1 = #count{ S,M : student_placement(S,M,W,upper) } 1.
% Lower position on each wall: exactly one painting
:- wall(W), not 1 = #count{ S,M : student_placement(S,M,W,lower) } 1.

% No wall has only watercolors displayed on it.
% i.e., each wall must have at least one oil painting
:- wall(W), #count{ S : student_placement(S,oil,W,_) } = 0.

% No wall has the work of only one student displayed on it.
% i.e., each wall must have paintings by at least two different students
:- wall(W), #count{ S : student_placement(S,_,W,_) } <= 1.

% No wall has both a painting by Franz and a painting by Isaacs displayed on it.
:- wall(W), student_placement(franz,_,W,_), student_placement(isaacs,_,W,_).

% Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
% Let WallF be the wall where Franz's oil is.
% Then Greene's watercolor must be on the same wall, upper position.
:- student_placement(franz, oil, WallF, _), 
   not student_placement(greene, watercolor, WallF, upper).

% Isaacs's oil is displayed in the lower position of wall 4.
student_placement(isaacs, oil, 4, lower).

%%% DERIVED PREDICATES FOR ANSWER CHOICES %%%

% (A) Franz's watercolor is displayed on the same wall as Greene's oil.
same_wall_fw_go :- student_placement(franz, watercolor, W, _), student_placement(greene, oil, W, _).

% (B) Franz's watercolor is displayed on the same wall as Hidalgo's oil.
same_wall_fw_ho :- student_placement(franz, watercolor, W, _), student_placement(hidalgo, oil, W, _).

% (C) Greene's oil is displayed in an upper position.
greene_oil_upper :- student_placement(greene, oil, _, upper).

% (D) Hidalgo's watercolor is displayed in a lower position.
hidalgo_wc_lower :- student_placement(hidalgo, watercolor, _, lower).

% (E) Isaacs's watercolor is displayed on the same wall as Hidalgo's oil.
same_wall_iw_ho :- student_placement(isaacs, watercolor, W, _), student_placement(hidalgo, oil, W, _).

%%% Determine which option CANNOT be true %%%
% An option is "cannot be true" if in ALL valid models, it is false.
% We need to check each option: if it's impossible (unsat when forced true), then it's the answer.

% We'll use a trick: for each option, we add a constraint forcing it to be true.
% If the whole program becomes UNSAT, then that option cannot be true.

% But we need to do this in one run. We'll use choice rules to test each option.

% Let's define a "test" predicate for each option.
% We'll use #show to see which options are possible.

% Actually, simpler: we can just check each option individually by running separate programs.
% But the instructions say one file. Let's use a different approach.

% We can use the fact that if an option is impossible, then forcing it leads to unsat.
% We'll create a meta-encoding.

% For each option, we create a scenario where we force it true and check satisfiability.
% We'll use a choice rule to select which option to test, and then check.

% Better approach: Since we need to find which one CANNOT be true,
% we can check each option by adding a constraint that makes it true,
% and see if the program is satisfiable.

% Let's do this with a single program using a "test" atom.

% We'll test each option one at a time by using a choice over test_option/1.
{ test_option(a) }. { test_option(b) }. { test_option(c) }. { test_option(d) }. { test_option(e) }.

% At most one test at a time
:- #count{ O : test_option(O) } > 1.

% Force the tested option to be true
:- test_option(a), not same_wall_fw_go.
:- test_option(b), not same_wall_fw_ho.
:- test_option(c), not greene_oil_upper.
:- test_option(d), not hidalgo_wc_lower.
:- test_option(e), not same_wall_iw_ho.

% If the program is satisfiable with test_option(X), then X is possible.
% If UNSAT, then X cannot be true.

% We want to find which option makes the program UNSAT when forced.
% Since we can't directly detect UNSAT in ASP, we'll use a different approach.

% Let's just enumerate all possible models and see which options are never true.

% Actually, let's use a simpler approach: just run the base program and see
% what assignments are possible. We'll show all relevant atoms.

#show student_placement/4.
#show same_wall_fw_go/0.
#show same_wall_fw_ho/0.
#show greene_oil_upper/0.
#show hidalgo_wc_lower/0.
#show same_wall_iw_ho/0.