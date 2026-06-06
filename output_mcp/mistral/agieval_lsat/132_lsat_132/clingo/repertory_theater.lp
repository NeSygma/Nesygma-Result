% Define movies
movie(horror).
movie(mystery).
movie(romance).
movie("sci-fi").
movie(western).

% Define screens
screen(1..3).

% Define time slots
time(7pm).
time(8pm).
time(9pm).

% Time ordering: earlier time comes before later time
before(7pm, 8pm).
before(8pm, 9pm).

% Each movie is shown exactly once on some screen and time
1 { assigned(M, S, T) : screen(S), time(T) } 1 :- movie(M).

% Screen 1 has exactly two movies: one at 7pm and one at 9pm
1 { assigned(M, 1, 7pm) : movie(M) } 1.
1 { assigned(M, 1, 9pm) : movie(M) } 1.

% Screen 2 has exactly two movies: one at 7pm and one at 9pm
1 { assigned(M, 2, 7pm) : movie(M) } 1.
1 { assigned(M, 2, 9pm) : movie(M) } 1.

% Screen 3 has exactly one movie at 8pm
1 { assigned(M, 3, 8pm) : movie(M) } 1.

% Constraint 1: Western begins before horror film
:- assigned(western, _, T_w), assigned(horror, _, T_h), before(T_h, T_w).

% Constraint 2: Sci-fi film is not shown on screen 3
:- assigned("sci-fi", 3, _).

% Constraint 3: Romance is not shown on screen 2
:- assigned(romance, 2, _).

% Constraint 4: Horror film and mystery are shown on different screens
:- assigned(horror, S, _), assigned(mystery, S, _).

% Define what each option means in terms of screen 1 assignments
possible_a :- assigned("sci-fi", 1, 7pm), assigned(horror, 1, 9pm).
possible_b :- assigned("sci-fi", 1, 7pm), assigned(mystery, 1, 9pm).
possible_c :- assigned(western, 1, 7pm), assigned(horror, 1, 9pm).
possible_d :- assigned(western, 1, 7pm), assigned(mystery, 1, 9pm).
possible_e :- assigned(western, 1, 7pm), assigned("sci-fi", 1, 9pm).

% The answer is the option that is NOT possible (i.e., cannot be accurate)
% Since we want the option that CANNOT be accurate, we mark it as the answer if it is impossible
option(a) :- not possible_a.
option(b) :- not possible_b.
option(c) :- not possible_c.
option(d) :- not possible_d.
option(e) :- not possible_e.

#show option/1.