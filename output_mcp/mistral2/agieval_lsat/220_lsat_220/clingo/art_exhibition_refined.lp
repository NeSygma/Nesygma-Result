% Define the students and painting types
student(franz; greene; hidalgo; isaacs).
wall(1; 2; 3; 4).
position(upper; lower).
painting_type(oil; watercolor).

% Each wall has exactly two paintings: one in upper and one in lower position
1 { painting_on(Wall, Position, Student, Type) : student(Student), painting_type(Type) } 1 :-
    wall(Wall), position(Position).

% No wall has only watercolors
:- wall(Wall), 
   { painting_on(Wall, _, _, watercolor) } = 2.

% No wall has the work of only one student
:- wall(Wall), 
   { painting_on(Wall, _, Student, _) : student(Student) } = 1.

% No wall has both a painting by Franz and a painting by Isaacs
:- wall(Wall), 
   painting_on(Wall, _, franz, _), 
   painting_on(Wall, _, isaacs, _).

% Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed
:- painting_on(Wall, upper, franz, oil),
   not painting_on(Wall, upper, greene, watercolor).

% Isaacs's oil is displayed in the lower position of wall 4
:- not painting_on(4, lower, isaacs, oil).

% Given conditions:
% Isaacs's watercolor is displayed on wall 2
painting_on(2, upper, isaacs, watercolor).

% Franz's oil is displayed on wall 3
painting_on(3, upper, franz, oil).

% Ensure each student has exactly one oil and one watercolor displayed
% (This is implicitly enforced by the constraints above, but we can add explicit checks)
student_painting_type(Student, Type) :- 
    student(Student), 
    painting_type(Type), 
    1 { painting_on(_, _, Student, Type) } 1.

% Ensure each student has exactly one oil and one watercolor
:- student(Student), 
   not student_painting_type(Student, oil).
:- student(Student), 
   not student_painting_type(Student, watercolor).

% Define what is displayed on wall 1
wall1_upper(Student, Type) :- painting_on(1, upper, Student, Type).
wall1_lower(Student, Type) :- painting_on(1, lower, Student, Type).

% The answer must be one of the following:
% (A) Franz's watercolor
% (B) Greene's oil
% (C) Greene's watercolor
% (D) Hidalgo's oil
% (E) Hidalgo's watercolor

% Check which option is true for wall 1
option(a) :- wall1_upper(franz, watercolor).
option(b) :- wall1_upper(greene, oil).
option(c) :- wall1_upper(greene, watercolor).
option(d) :- wall1_upper(hidalgo, oil).
option(e) :- wall1_upper(hidalgo, watercolor).

#show option/1.