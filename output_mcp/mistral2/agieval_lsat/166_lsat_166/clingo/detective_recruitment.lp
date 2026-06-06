% Base facts: time steps and accomplices
accomplice(peters).
accomplice(quinn).
accomplice(rovero).
accomplice(stanton).
accomplice(tao).
accomplice(villas).
accomplice(white).

% Time steps (1 to 7)
time(1..7).

% Each time step has exactly one accomplice recruited
1 { recruited(A, T) : accomplice(A) } 1 :- time(T).

% Each accomplice is recruited exactly once
:- accomplice(A), 2 { recruited(A, T) : time(T) }.

% Peters was recruited fourth
recruited(peters, 4).

% Villas was recruited immediately before White
:- recruited(villas, T), not recruited(white, T+1), time(T+1).
:- recruited(white, T), not recruited(villas, T-1), time(T-1).

% Quinn was recruited earlier than Rovero
:- recruited(rovero, T2), time(T1), T1 < T2, not recruited(quinn, T1).

% Stanton was recruited neither immediately before nor immediately after Tao
:- recruited(stanton, T), recruited(tao, T+1).
:- recruited(stanton, T), recruited(tao, T-1).
:- recruited(tao, T), recruited(stanton, T+1).
:- recruited(tao, T), recruited(stanton, T-1).

% Additional constraints from the question:
% White was recruited earlier than Rovero
:- recruited(rovero, T2), time(T1), T1 < T2, not recruited(white, T1).

% Rovero was recruited earlier than Tao
:- recruited(tao, T2), time(T1), T1 < T2, not recruited(rovero, T1).

% Define the order of recruitment as a list for clarity
order(T, A) :- recruited(A, T).

% --- Multiple Choice Options ---
% (A) Quinn was recruited first.
option(a) :- recruited(quinn, 1).

% (B) Rovero was recruited third.
option(b) :- recruited(rovero, 3).

% (C) Stanton was recruited second.
option(c) :- recruited(stanton, 2).

% (D) Tao was recruited sixth.
option(d) :- recruited(tao, 6).

% (E) Villas was recruited sixth.
option(e) :- recruited(villas, 6).

#show option/1.