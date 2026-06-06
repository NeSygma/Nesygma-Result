% Base facts: students, painting types, walls, and positions
student(franz; greene; hidalgo; isaacs).
type(oil; watercolor).
wall(1; 2; 3; 4).
position(upper; lower).

% Each wall has exactly two paintings: one in upper and one in lower position
% This is enforced by the choice rule below.
1 { painting_on(Wall, Position, Student, Type) : student(Student), type(Type) } 1 :-
    wall(Wall), position(Position).

% No wall has only watercolors
:- wall(Wall),
   not (painting_on(Wall, upper, _, oil) ; painting_on(Wall, lower, _, oil)).

% No wall has the work of only one student
:- wall(Wall),
   not 2 { painting_on(Wall, _, Student, _) : student(Student) }.

% No wall has both a painting by Franz and a painting by Isaacs
:- wall(Wall),
   painting_on(Wall, _, franz, _),
   painting_on(Wall, _, isaacs, _).

% Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed
:- painting_on(Wall, upper, franz, oil),
   not painting_on(Wall, upper, greene, watercolor).

% Isaacs's oil is displayed in the lower position of wall 4
:- not painting_on(4, lower, isaacs, oil).

% Helper predicate: Greene's oil is on the same wall as Franz's watercolor
same_wall_greene_oil_franz_water(Wall) :-
    painting_on(Wall, _, franz, watercolor),
    painting_on(Wall, upper, greene, oil).

% Enforce the condition: Greene's oil is displayed on the same wall as Franz's watercolor
% This is the condition for the question
:- not same_wall_greene_oil_franz_water(Wall), wall(Wall).

% Now, derive the answer based on the condition
% (A) Greene's oil is displayed in an upper position.
option(a) :-
    same_wall_greene_oil_franz_water(Wall),
    painting_on(Wall, upper, greene, oil).

% (B) Hidalgo's watercolor is displayed on the same wall as Isaacs's watercolor.
option(b) :-
    same_wall_greene_oil_franz_water(Wall),
    painting_on(Wall, _, hidalgo, watercolor),
    painting_on(Wall, _, isaacs, watercolor).

% (C) Hidalgo's oil is displayed in an upper position.
option(c) :-
    same_wall_greene_oil_franz_water(Wall),
    painting_on(Wall, upper, hidalgo, oil).

% (D) Hidalgo's oil is displayed on the same wall as Isaacs's watercolor.
option(d) :-
    same_wall_greene_oil_franz_water(Wall),
    painting_on(Wall, _, hidalgo, oil),
    painting_on(Wall, _, isaacs, watercolor).

% (E) Isaacs's watercolor is displayed in a lower position.
option(e) :-
    same_wall_greene_oil_franz_water(Wall),
    painting_on(Wall, lower, isaacs, watercolor).

#show option/1.