% Define the students and their paintings
student(franz; greene; hidalgo; isaacs).
medium(oil; watercolor).
wall(1; 2; 3; 4).
position(upper; lower).

% Each student displays exactly two paintings: one oil and one watercolor
% This is implicitly enforced by the assignment constraints below.

% Each wall has exactly two paintings: one in upper and one in lower position
1 { painting_on(Wall, Position, Student, Medium) : student(Student), medium(Medium) } 1 :-
    wall(Wall), position(Position).

% No wall has only watercolors displayed on it
:- wall(Wall),
    not painting_on(Wall, upper, _, oil),
    not painting_on(Wall, lower, _, oil).

% No wall has the work of only one student displayed on it
:- wall(Wall),
    student(S),
    not painting_on(Wall, upper, S, _),
    not painting_on(Wall, lower, S, _),
    painting_on(Wall, upper, _, _),
    painting_on(Wall, lower, _, _).

% No wall has both a painting by Franz and a painting by Isaacs displayed on it
:- wall(Wall),
    painting_on(Wall, _, franz, _),
    painting_on(Wall, _, isaacs, _).

% Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed
:- painting_on(Wall, upper, greene, watercolor),
    not painting_on(Wall, _, franz, oil).
:- not painting_on(Wall, upper, greene, watercolor),
    painting_on(Wall, _, franz, oil).

% Isaacs's oil is displayed in the lower position of wall 4
:- not painting_on(4, lower, isaacs, oil).

% Additional constraints to ensure each student has exactly one oil and one watercolor
% (This is implicitly enforced by the problem statement, but we can add a check)
:- student(Student),
    #count { Medium : painting_on(_, _, Student, Medium) } != 2.

:- student(Student),
    #count { Medium : painting_on(_, _, Student, Medium), Medium = oil } != 1.

:- student(Student),
    #count { Medium : painting_on(_, _, Student, Medium), Medium = watercolor } != 1.

% --- Multiple Choice Options ---
% Define helper predicates for each option

% Option A: Both of Franz's paintings and both of Greene's paintings are displayed in lower positions.
option(a) :-
    painting_on(Wall1, lower, franz, oil),
    painting_on(Wall2, lower, franz, watercolor),
    painting_on(Wall3, lower, greene, oil),
    painting_on(Wall4, lower, greene, watercolor).

% Option B: Both of Franz's paintings and both of Greene's paintings are displayed in upper positions.
option(b) :-
    painting_on(Wall1, upper, franz, oil),
    painting_on(Wall2, upper, franz, watercolor),
    painting_on(Wall3, upper, greene, oil),
    painting_on(Wall4, upper, greene, watercolor).

% Option C: Both of Franz's paintings and both of Hidalgo's paintings are displayed in upper positions.
option(c) :-
    painting_on(Wall1, upper, franz, oil),
    painting_on(Wall2, upper, franz, watercolor),
    painting_on(Wall3, upper, hidalgo, oil),
    painting_on(Wall4, upper, hidalgo, watercolor).

% Option D: Both of Greene's paintings and both of Hidalgo's paintings are displayed in lower positions.
option(d) :-
    painting_on(Wall1, lower, greene, oil),
    painting_on(Wall2, lower, greene, watercolor),
    painting_on(Wall3, lower, hidalgo, oil),
    painting_on(Wall4, lower, hidalgo, watercolor).

% Option E: Both of Greene's paintings and both of Hidalgo's paintings are displayed in upper positions.
option(e) :-
    painting_on(Wall1, upper, greene, oil),
    painting_on(Wall2, upper, greene, watercolor),
    painting_on(Wall3, upper, hidalgo, oil),
    painting_on(Wall4, upper, hidalgo, watercolor).

#show option/1.