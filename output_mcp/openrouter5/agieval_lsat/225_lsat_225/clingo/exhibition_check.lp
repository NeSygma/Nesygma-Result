%%% DOMAIN DEFINITIONS %%%

% Students
student(franz; greene; hidalgo; isaacs).

% Walls
wall(1;2;3;4).

% Positions
position(upper; lower).

%%% CHOICE RULES: Assign each student's two paintings to walls and positions %%%

% Student's oil: assigned to exactly one wall and one position
{ student_placement(Student, oil, Wall, Pos) : wall(Wall), position(Pos) } 1 :- student(Student).

% Student's watercolor: assigned to exactly one wall and one position
{ student_placement(Student, watercolor, Wall, Pos) : wall(Wall), position(Pos) } 1 :- student(Student).

%%% CONSTRAINTS %%%

% Exactly two paintings on each wall (one upper, one lower)
:- wall(W), #count{ S,M : student_placement(S,M,W,upper) } != 1.
:- wall(W), #count{ S,M : student_placement(S,M,W,lower) } != 1.

% No wall has only watercolors displayed on it (each wall must have at least one oil)
:- wall(W), #count{ S : student_placement(S,oil,W,_) } = 0.

% No wall has the work of only one student displayed on it.
:- wall(W), #count{ S : student_placement(S,_,W,_) } <= 1.

% No wall has both a painting by Franz and a painting by Isaacs displayed on it.
:- wall(W), student_placement(franz,_,W,_), student_placement(isaacs,_,W,_).

% Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
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
% An option is "possible" if there exists at least one model where it holds.
% We need to find which one is impossible.

% We'll use a different approach: check each option individually by adding a constraint
% that forces it to be true, and see which one is UNSAT.

% For now, let's just show all derived predicates to analyze.
#show student_placement/4.
#show same_wall_fw_go/0.
#show same_wall_fw_ho/0.
#show greene_oil_upper/0.
#show hidalgo_wc_lower/0.
#show same_wall_iw_ho/0.