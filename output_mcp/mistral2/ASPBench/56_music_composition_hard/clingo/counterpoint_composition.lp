% --- DOMAINS ---
time(1..8).
voice(soprano; alto).
note(c; d; e; f; g; a; b).
octave(soprano,4..5).
octave(alto,3..4).

% MIDI mapping for notes and octaves
midi(c,4,60). midi(d,4,62). midi(e,4,64). midi(f,4,65). midi(g,4,67). midi(a,4,69). midi(b,4,71).
midi(c,5,72). midi(d,5,74). midi(e,5,76). midi(f,5,77). midi(g,5,79). midi(a,5,81). midi(b,5,83).
midi(e,3,52). midi(f,3,53). midi(g,3,55). midi(a,3,57). midi(b,3,59). midi(c,4,60). midi(d,4,62). midi(e,4,64).

% Chord definitions
chord(v,g;b;d).
chord(i,c;e;g).

% Allowed harmonic intervals (semitones)
allowed_harmonic_interval(3). allowed_harmonic_interval(4).
allowed_harmonic_interval(7).
allowed_harmonic_interval(8). allowed_harmonic_interval(9).
allowed_harmonic_interval(12).
allowed_harmonic_interval(15). allowed_harmonic_interval(16).

% --- CHOICE RULE ---
% Choose exactly one note and octave for each voice at each time step
{ selected_note(V, T, N, O) : note(N), octave(V,O) } 1 :- voice(V), time(T).

% --- DERIVED PREDICATES ---
% Pitch in MIDI
pitch(V, T, P) :- selected_note(V, T, N, O), midi(N, O, P).

% Harmonic interval at each time step
harmonic_interval(T, I) :- pitch(soprano, T, P1), pitch(alto, T, P2), I = P1 - P2, allowed_harmonic_interval(I).

% Voice crossing: soprano <= alto
voice_crossing(T) :- pitch(soprano, T, P1), pitch(alto, T, P2), P1 =< P2.

% Melodic leap: > perfect fifth (7 semitones)
melodic_leap(V, T) :- pitch(V, T, P1), pitch(V, T+1, P2), abs(P1 - P2) > 7, time(T+1).

% Parallel fifths/octaves between consecutive time steps
parallel_fifths(T) :- harmonic_interval(T, 7), harmonic_interval(T+1, 7), time(T+1).
parallel_octaves(T) :- harmonic_interval(T, 12), harmonic_interval(T+1, 12), time(T+1).

% Cadence at time 7: both notes in V-chord
cadence(T) :- time(T), T = 7, chord(v, N1), chord(v, N2), selected_note(soprano, T, N1, _), selected_note(alto, T, N2, _).

% Resolution at time 8: soprano on C5, alto on C4
resolution(T) :- time(T), T = 8, selected_note(soprano, T, c, 5), selected_note(alto, T, c, 4).

% --- CONSTRAINTS ---
% 1. No voice crossing
:- voice_crossing(T), time(T).

% 2. No melodic leaps > perfect fifth
:- melodic_leap(V, T), voice(V), time(T).

% 3. No parallel fifths or octaves
:- parallel_fifths(T), time(T+1).
:- parallel_octaves(T), time(T+1).

% 4. Cadence at time 7
:- not cadence(7).

% 5. Resolution at time 8
:- not resolution(8).

% 6. Starting notes: Alto on C4 at time 1
:- not selected_note(alto, 1, c, 4).

% 7. Starting notes: Soprano on E4 or G4 at time 1
:- not selected_note(soprano, 1, e, 4).
:- not selected_note(soprano, 1, g, 4).

% --- ANALYSIS PREDICATES ---
% Count parallel fifths/octaves/voice crossings
count_parallel_fifths(N) :- N = #count { T : parallel_fifths(T) }.
count_parallel_octaves(N) :- N = #count { T : parallel_octaves(T) }.
count_voice_crossings(N) :- N = #count { T : voice_crossing(T) }.

% --- OUTPUT ---
#show selected_note/4.
#show count_parallel_fifths/1.
#show count_parallel_octaves/1.
#show count_voice_crossings/1.