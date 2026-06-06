% Define the students and their paintings
student(franz; greene; hidalgo; isaacs).
medium(oil; watercolor).
wall(1; 2; 3; 4).
position(upper; lower).

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
% This means: If Franz's oil is on a wall, then Greene's watercolor must be on the upper position of that wall.
greene_watercolor_upper_on_franz_oil_wall(Wall) :-
    painting_on(Wall, _, franz, oil),
    painting_on(Wall, upper, greene, watercolor).

:- painting_on(Wall, _, franz, oil),
    not greene_watercolor_upper_on_franz_oil_wall(Wall).

% Isaacs's oil is displayed in the lower position of wall 4
:- not painting_on(4, lower, isaacs, oil).

% Ensure each student has exactly one oil and one watercolor
:- student(Student),
    #count { Medium : painting_on(_, _, Student, Medium) } != 2.

:- student(Student),
    #count { Medium : painting_on(_, _, Student, Medium), Medium = oil } != 1.

:- student(Student),
    #count { Medium : painting_on(_, _, Student, Medium), Medium = watercolor } != 1.

% --- Multiple Choice Options ---
% Define helper predicates for each option

% Option A: Both of Franz's paintings and both of Greene's paintings are displayed in lower positions.
% This means Franz's oil and watercolor are both in lower positions, and Greene's oil and watercolor are both in lower positions.
option(a) :-
    painting_on(W1, lower, franz, oil),
    painting_on(W2, lower, franz, watercolor),
    W1 != W2,
    painting_on(W3, lower, greene, oil),
    painting_on(W4, lower, greene, watercolor),
    W3 != W4.

% Option B: Both of Franz's paintings and both of Greene's paintings are displayed in upper positions.
option(b) :-
    painting_on(W1, upper, franz, oil),
    painting_on(W2, upper, franz, watercolor),
    W1 != W2,
    painting_on(W3, upper, greene, oil),
    painting_on(W4, upper, greene, watercolor),
    W3 != W4.

% Option C: Both of Franz's paintings and both of Hidalgo's paintings are displayed in upper positions.
option(c) :-
    painting_on(W1, upper, franz, oil),
    painting_on(W2, upper, franz, watercolor),
    W1 != W2,
    painting_on(W3, upper, hidalgo, oil),
    painting_on(W4, upper, hidalgo, watercolor),
    W3 != W4.

% Option D: Both of Greene's paintings and both of Hidalgo's paintings are displayed in lower positions.
option(d) :-
    painting_on(W1, lower, greene, oil),
    painting_on(W2, lower, greene, watercolor),
    W1 != W2,
    painting_on(W3, lower, hidalgo, oil),
    painting_on(W4, lower, hidalgo, watercolor),
    W3 != W4.

% Option E: Both of Greene's paintings and both of Hidalgo's paintings are displayed in upper positions.
option(e) :-
    painting_on(W1, upper, greene, oil),
    painting_on(W2, upper, greene, watercolor),
    W1 != W2,
    painting_on(W3, upper, hidalgo, oil),
    painting_on(W4, upper, hidalgo, watercolor),
    W3 != W4.

#show option/1.