% Counterpoint Composition in C Major
% Soprano and Alto voices, 8 time steps

% ==================== DOMAIN DECLARATIONS ====================

% Notes in C Major scale with MIDI numbers
note("C", 3, 48). note("C", 4, 60). note("C", 5, 72).
note("D", 3, 50). note("D", 4, 62). note("D", 5, 74).
note("E", 3, 52). note("E", 4, 64). note("E", 5, 76).
note("F", 3, 53). note("F", 4, 65). note("F", 5, 77).
note("G", 3, 55). note("G", 4, 67). note("G", 5, 79).
note("A", 3, 57). note("A", 4, 69). note("A", 5, 81).
note("B", 3, 59). note("B", 4, 71). note("B", 5, 83).

% Voices
voice(soprano). voice(alto).

% Time steps
time(1..8).

% ==================== VOICE RANGES ====================

% Soprano range: C4 (60) to A5 (81)
valid_note(soprano, N, O) :- note(N, O, M), M >= 60, M <= 81.

% Alto range: E3 (52) to C5 (72)
valid_note(alto, N, O) :- note(N, O, M), M >= 52, M <= 72.

% ==================== NOTE ASSIGNMENT ====================

% Choice rule: each voice at each time gets exactly one valid note
{ note_at(V, T, N, O) : note(N, O, M), valid_note(V, N, O) } 1 :- voice(V), time(T).

% Derive MIDI numbers from note assignments
midi_at(V, T, M) :- note_at(V, T, N, O), note(N, O, M).

% ==================== CONSTRAINTS ====================

% 1. C Major scale: Already enforced by note definitions

% 2. Voice ranges: Already enforced by valid_note/3

% 3. No voice crossing: Soprano must be strictly higher than Alto
:- time(T), midi_at(soprano, T, M1), midi_at(alto, T, M2), M1 <= M2.

% 4. Melodic leaps: Consecutive notes must not exceed perfect fifth (7 semitones)
melodic_interval(V, T, I) :- time(T), time(T1), T1 = T + 1, 
                              midi_at(V, T, M1), midi_at(V, T1, M2), 
                              I = M2 - M1, I >= 0.
melodic_interval(V, T, I) :- time(T), time(T1), T1 = T + 1, 
                              midi_at(V, T, M1), midi_at(V, T1, M2), 
                              I = M1 - M2, I >= 0.
:- melodic_interval(V, T, I), I > 7.

% 5. Harmonic consonances: Allowed intervals
allowed_interval(3). allowed_interval(4). allowed_interval(7). 
allowed_interval(8). allowed_interval(9). allowed_interval(12).
allowed_interval(15). allowed_interval(16).

% Calculate harmonic interval at each time
interval_semitones(T, I) :- time(T), 
                            midi_at(soprano, T, M1), midi_at(alto, T, M2),
                            I = M1 - M2, I > 0.
:- interval_semitones(T, I), not allowed_interval(I).

% 6. No parallel motion: No parallel perfect fifths or octaves
% Parallel fifth: interval = 7 at both times
parallel_fifth(T1, T2) :- time(T1), time(T2), T2 = T1 + 1,
                          interval_semitones(T1, 7), interval_semitones(T2, 7).
% Parallel octave: interval = 12 at both times
parallel_octave(T1, T2) :- time(T1), time(T2), T2 = T1 + 1,
                           interval_semitones(T1, 12), interval_semitones(T2, 12).
:- parallel_fifth(T1, T2).
:- parallel_octave(T1, T2).

% 7. Starting notes: Time 1 constraints
% Alto must be on C4 (MIDI 60)
:- time(1), midi_at(alto, 1, M), M != 60.
% Soprano must be on E4 (64) or G4 (67)
:- time(1), midi_at(soprano, 1, M), M != 64, M != 67.

% 8. Cadence at time 7: Both notes must belong to V-chord (G, B, D)
% V-chord notes: G (55,67,79), B (59,71,83), D (50,62,74)
v_chord_note(M) :- note("G", _, M); note("B", _, M); note("D", _, M).
:- time(7), midi_at(soprano, 7, M1), not v_chord_note(M1).
:- time(7), midi_at(alto, 7, M2), not v_chord_note(M2).

% 9. Final resolution at time 8: Soprano C5 (72), Alto C4 (60)
:- time(8), midi_at(soprano, 8, M), M != 72.
:- time(8), midi_at(alto, 8, M), M != 60.

% ==================== VALID SOLUTION ====================
valid_solution :- time(1), time(8). % If all constraints satisfied, solution exists

% ==================== OUTPUT ====================
% Show the composition
#show note_at/4.
#show interval_semitones/2.
#show valid_solution/0.

% Analysis summary
parallel_fifth_count(N) :- N = #count{T1, T2 : parallel_fifth(T1, T2)}.
parallel_octave_count(N) :- N = #count{T1, T2 : parallel_octave(T1, T2)}.
voice_crossing_count(N) :- N = #count{T : voice_crossing(T)}.

#show parallel_fifth_count/1.
#show parallel_octave_count/1.
#show voice_crossing_count/1.