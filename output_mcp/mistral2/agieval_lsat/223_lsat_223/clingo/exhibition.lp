% Base facts: students, paintings, walls, and positions
student(franz; greene; hidalgo; isaacs).
painting(oil; watercolor).
wall(1; 2; 3; 4).
position(upper; lower).

% Each student displays exactly two paintings: one oil and one watercolor
% This is enforced by the assignment constraints below.

% Each wall has exactly two paintings: one in upper and one in lower position
1 { assigned(Wall, Position, Student, Painting) : student(Student), painting(Painting) } 2 :-
    wall(Wall), position(Position).

% Ensure each student has exactly one oil and one watercolor
:- student(Student), 
   #count{Wall, Position : assigned(Wall, Position, Student, oil)} != 1.
:- student(Student), 
   #count{Wall, Position : assigned(Wall, Position, Student, watercolor)} != 1.

% No wall has only watercolors
:- wall(Wall), 
   #count{Position : assigned(Wall, Position, _, watercolor)} = 2.

% No wall has the work of only one student
:- wall(Wall), 
   #count{Student : assigned(Wall, _, Student, _)} = 1.

% No wall has both a painting by Franz and a painting by Isaacs
:- wall(Wall), 
   assigned(Wall, _, franz, _), 
   assigned(Wall, _, isaacs, _).

% Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed
:- assigned(Wall, upper, franz, oil),
   not assigned(Wall, upper, greene, watercolor).

% Isaacs's oil is displayed in the lower position of wall 4
:- not assigned(4, lower, isaacs, oil).

% If Franz's oil is displayed on wall 1
% (This is the condition for the question)
:- not assigned(1, _, franz, oil).

% --- Mapping the answer choices to option/1 ---
% (A) Franz's watercolor is displayed on wall 4
option(a) :- assigned(4, _, franz, watercolor).

% (B) Greene's oil is displayed on wall 2
option(b) :- assigned(2, _, greene, oil).

% (C) Greene's watercolor is displayed on wall 2
option(c) :- assigned(2, _, greene, watercolor).

% (D) Hidalgo's watercolor is displayed on wall 3
option(d) :- assigned(3, _, hidalgo, watercolor).

% (E) Isaacs's oil is displayed on wall 1
option(e) :- assigned(1, _, isaacs, oil).

#show option/1.