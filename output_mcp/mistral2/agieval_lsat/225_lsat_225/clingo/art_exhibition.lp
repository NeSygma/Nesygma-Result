% Define the students and painting types
student(franz; greene; hidalgo; isaacs).
wall(1; 2; 3; 4).
position(upper; lower).
painting_type(oil; watercolor).

% Each student displays exactly two paintings: one oil and one watercolor
% This is implicitly enforced by the assignment constraints below.

% Each wall has exactly two paintings: one in upper and one in lower position
1 { assignment(Wall, Position, Student, PaintingType) : 
        student(Student), 
        painting_type(PaintingType) 
    } 1 :-
    wall(Wall), 
    position(Position).

% Ensure each student has exactly one oil and one watercolor displayed
% (This is enforced by the assignment constraints and the uniqueness of positions)

% No wall has only watercolors displayed on it
:- wall(Wall), 
   position(upper), 
   position(lower),
   assignment(Wall, upper, _, watercolor),
   assignment(Wall, lower, _, watercolor).

% No wall has the work of only one student displayed on it
:- wall(Wall),
   assignment(Wall, upper, S1, _),
   assignment(Wall, lower, S2, _),
   S1 != S2.

% No wall has both a painting by Franz and a painting by Isaacs displayed on it
:- wall(Wall),
   assignment(Wall, upper, franz, _),
   assignment(Wall, lower, isaacs, _).
:- wall(Wall),
   assignment(Wall, upper, isaacs, _),
   assignment(Wall, lower, franz, _).

% Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed
:- assignment(Wall, upper, greene, watercolor),
   not assignment(Wall, _, franz, oil).

% Isaacs's oil is displayed in the lower position of wall 4
:- not assignment(4, lower, isaacs, oil).

% Additional constraint: Franz's oil must be displayed somewhere
:- not assignment(_, _, franz, oil).

% Additional constraint: Greene's watercolor must be displayed somewhere
:- not assignment(_, _, greene, watercolor).

% Additional constraint: Isaacs's watercolor must be displayed somewhere
:- not assignment(_, _, isaacs, watercolor).

% Additional constraint: Hidalgo's oil and watercolor must be displayed somewhere
:- not assignment(_, _, hidalgo, oil).
:- not assignment(_, _, hidalgo, watercolor).

% --- Define the multiple choice options ---

% (A) Franz's watercolor is displayed on the same wall as Greene's oil
option(a) :- wall(Wall),
             assignment(Wall, _, franz, watercolor),
             assignment(Wall, _, greene, oil).

% (B) Franz's watercolor is displayed on the same wall as Hidalgo's oil
option(b) :- wall(Wall),
             assignment(Wall, _, franz, watercolor),
             assignment(Wall, _, hidalgo, oil).

% (C) Greene's oil is displayed in an upper position
option(c) :- wall(Wall),
             assignment(Wall, upper, greene, oil).

% (D) Hidalgo's watercolor is displayed in a lower position
option(d) :- wall(Wall),
             assignment(Wall, lower, hidalgo, watercolor).

% (E) Isaacs's watercolor is displayed on the same wall as Hidalgo's oil
option(e) :- wall(Wall),
             assignment(Wall, _, isaacs, watercolor),
             assignment(Wall, _, hidalgo, oil).

#show option/1.