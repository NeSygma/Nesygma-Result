% Time steps
time(1..8).

% MIDI Note definitions
note(N) :- N = 0..127.
is_c_major(N) :- note(N), N \ 12 = 0.
is_c_major(N) :- note(N), N \ 12 = 2.
is_c_major(N) :- note(N), N \ 12 = 4.
is_c_major(N) :- note(N), N \ 12 = 5.
is_c_major(N) :- note(N), N \ 12 = 7.
is_c_major(N) :- note(N), N \ 12 = 9.
is_c_major(N) :- note(N), N \ 12 = 11.

% Ranges
soprano_range(N) :- N >= 60, N <= 81, is_c_major(N).
alto_range(N) :- N >= 52, N <= 72, is_c_major(N).

% Generation
{ soprano(N, T) : soprano_range(N) } = 1 :- time(T).
{ alto(N, T) : alto_range(N) } = 1 :- time(T).

% Constraints
% 1. No voice crossing
:- soprano(S, T), alto(A, T), S <= A.

% 2. Melodic leaps <= 7 semitones
:- soprano(S1, T), soprano(S2, T+1), time(T), S1 > S2, S1 - S2 > 7.
:- soprano(S1, T), soprano(S2, T+1), time(T), S2 > S1, S2 - S1 > 7.
:- alto(A1, T), alto(A2, T+1), time(T), A1 > A2, A1 - A2 > 7.
:- alto(A1, T), alto(A2, T+1), time(T), A2 > A1, A2 - A1 > 7.

% 3. Harmonic consonances
harmonic_interval(3; 4; 7; 8; 9; 12; 15; 16).
:- soprano(S, T), alto(A, T), I = S - A, not harmonic_interval(I).

% 4. No parallel motion (5ths and 8ves)
:- soprano(S1, T), alto(A1, T), soprano(S2, T+1), alto(A2, T+1), time(T), S1-A1 = 7, S2-A2 = 7.
:- soprano(S1, T), alto(A1, T), soprano(S2, T+1), alto(A2, T+1), time(T), S1-A1 = 12, S2-A2 = 12.

% 5. Starting notes (T=1)
:- alto(A, 1), A != 60.
:- soprano(S, 1), S != 64, S != 67.

% 6. Cadence at time 7 (V-chord: G, B, D)
v_chord(N) :- note(N), N \ 12 = 7.
v_chord(N) :- note(N), N \ 12 = 11.
v_chord(N) :- note(N), N \ 12 = 2.
:- soprano(S, 7), not v_chord(S).
:- alto(A, 7), not v_chord(A).

% 7. Final resolution at time 8 (Soprano C5=72, Alto C4=60)
:- soprano(S, 8), S != 72.
:- alto(A, 8), A != 60.

% Output
#show soprano/2.
#show alto/2.