% Define the time steps (1 to 7)
time(1..7).

% Define the accomplices
accomplice(peters).
accomplice(quinn).
accomplice(rovero).
accomplice(stanton).
accomplice(tao).
accomplice(villas).
accomplice(white).

% Assign each time step to an accomplice
% Use a choice rule to allow the solver to assign accomplices to time steps
{ assigned(T, A) : accomplice(A) } 1 :- time(T).

% Ensure each accomplice is assigned to exactly one time step
:- accomplice(A), time(T1), time(T2), T1 != T2, assigned(T1, A), assigned(T2, A).

% Peters was recruited fourth
:- not assigned(4, peters).

% Quinn was recruited earlier than Rovero
:- assigned(T1, quinn), assigned(T2, rovero), T1 >= T2.

% Villas was recruited immediately before White
:- assigned(T, villas), not assigned(T+1, white).
:- assigned(T, white), not assigned(T-1, villas).

% Stanton was recruited neither immediately before nor immediately after Tao
:- assigned(T, stanton), assigned(T+1, tao).
:- assigned(T, stanton), assigned(T-1, tao).
:- assigned(T, tao), assigned(T+1, stanton).
:- assigned(T, tao), assigned(T-1, stanton).

% Helper predicates to extract the order of accomplices
order(T, A) :- assigned(T, A).

% Define the middle five positions (2nd to 6th)
middle_pos(2..6).

% Define the options for the middle five positions
% Option A: Quinn, Stanton, Peters, Tao, Villas
% Note: Peters is fixed at position 4, so this option is invalid because Villas cannot be at position 6 if Peters is at 4 and Villas must be immediately before White.
% We still encode it for completeness.
option(a) :-
    order(2, quinn),
    order(3, stanton),
    order(4, peters),
    order(5, tao),
    order(6, villas),
    assigned(7, white).

% Option B: Quinn, Stanton, Peters, Tao, White
option(b) :-
    order(2, quinn),
    order(3, stanton),
    order(4, peters),
    order(5, tao),
    order(6, white),
    assigned(7, _).

% Option C: Villas, White, Peters, Quinn, Stanton
% Peters is fixed at position 4, so this option is invalid because Villas and White must be consecutive and before Peters.
option(c) :-
    order(2, villas),
    order(3, white),
    order(4, peters),
    order(5, quinn),
    order(6, stanton),
    assigned(1, _),
    assigned(7, _).

% Option D: Villas, White, Peters, Rovero, Stanton
option(d) :-
    order(2, villas),
    order(3, white),
    order(4, peters),
    order(5, rovero),
    order(6, stanton),
    assigned(1, _),
    assigned(7, _).

% Option E: Villas, White, Quinn, Rovero, Stanton
% Peters must be at position 4, so this option is invalid unless Quinn is at position 4, which conflicts with Peters.
option(e) :-
    order(2, villas),
    order(3, white),
    order(4, peters),
    order(5, quinn),
    order(6, rovero),
    assigned(1, stanton),
    assigned(7, tao).

#show option/1.