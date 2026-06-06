% ============================================
% Counterpoint Composition for Soprano and Alto
% 8 time steps, C Major key
% ============================================

% --- Domain Definitions ---

% Time steps
time(1..8).

% Voices
voice(soprano).
voice(alto).

% Notes in C Major scale
note(c). note(d). note(e). note(f). note(g). note(a). note(b).

% Semitone offsets from C
semitone(c, 0).
semitone(d, 2).
semitone(e, 4).
semitone(f, 5).
semitone(g, 7).
semitone(a, 9).
semitone(b, 11).

% Octave ranges for MIDI calculation
% Soprano: C4(60) to A5(81) - octaves 4 and 5
% Alto: E3(52) to C5(72) - octaves 3, 4, and 5

% Valid (voice, note, octave) combinations within range
% Soprano range: C4(60) to A5(81)
valid_note(soprano, c, 4).  % 60
valid_note(soprano, d, 4).  % 62
valid_note(soprano, e, 4).  % 64
valid_note(soprano, f, 4).  % 65
valid_note(soprano, g, 4).  % 67
valid_note(soprano, a, 4).  % 69
valid_note(soprano, b, 4).  % 71
valid_note(soprano, c, 5).  % 72
valid_note(soprano, d, 5).  % 74
valid_note(soprano, e, 5).  % 76
valid_note(soprano, f, 5).  % 77
valid_note(soprano, g, 5).  % 79
valid_note(soprano, a, 5).  % 81

% Alto range: E3(52) to C5(72)
valid_note(alto, e, 3).  % 52
valid_note(alto, f, 3).  % 53
valid_note(alto, g, 3).  % 55
valid_note(alto, a, 3).  % 57
valid_note(alto, b, 3).  % 59
valid_note(alto, c, 4).  % 60
valid_note(alto, d, 4).  % 62
valid_note(alto, e, 4).  % 64
valid_note(alto, f, 4).  % 65
valid_note(alto, g, 4).  % 67
valid_note(alto, a, 4).  % 69
valid_note(alto, b, 4).  % 71
valid_note(alto, c, 5).  % 72

% MIDI value calculation
midi_val(V, N, Oct, M) :- valid_note(V, N, Oct), semitone(N, S), M = Oct * 12 + S.

% --- Choice Rule: Assign notes to voices at each time step ---
{ note_at(V, T, N, Oct) : valid_note(V, N, Oct) } 1 :- voice(V), time(T).

% --- Derived: MIDI values for each voice at each time ---
midi(V, T, M) :- note_at(V, T, N, Oct), midi_val(V, N, Oct, M).

% --- Constraint 1: All notes must be from C Major scale (already enforced by valid_note) ---

% --- Constraint 2: Voice ranges (already enforced by valid_note) ---

% --- Constraint 3: No voice crossing - Soprano must be strictly higher ---
:- time(T), midi(soprano, T, Ms), midi(alto, T, Ma), Ms <= Ma.

% --- Constraint 4: Melodic leaps - no more than perfect fifth (7 semitones) ---
:- time(T), time(T+1), voice(V), midi(V, T, M1), midi(V, T+1, M2), 
   D = M2 - M1, |D| > 7.

% --- Constraint 5: Harmonic consonances ---
% Allowed: 3, 4, 7, 8, 9, 12, 15, 16 semitones
harmonic_interval(T, I) :- time(T), midi(soprano, T, Ms), midi(alto, T, Ma), I = Ms - Ma.
:- time(T), harmonic_interval(T, I), I != 3, I != 4, I != 7, I != 8, I != 9, I != 12, I != 15, I != 16.

% --- Constraint 6: No parallel perfect fifths or octaves ---
% Parallel fifths: both consecutive intervals are 7
:- time(T), time(T+1), harmonic_interval(T, 7), harmonic_interval(T+1, 7).
% Parallel octaves: both consecutive intervals are 12
:- time(T), time(T+1), harmonic_interval(T, 12), harmonic_interval(T+1, 12).

% --- Constraint 7: Starting notes at time 1 ---
% Alto must be on C4
note_at(alto, 1, c, 4).
% Soprano must be on E4 or G4
{ note_at(soprano, 1, e, 4); note_at(soprano, 1, g, 4) } 1.

% --- Constraint 8: Cadence at time 7 - both on V-chord (G, B, D) ---
:- time(7), note_at(soprano, 7, N, _), N != g, N != b, N != d.
:- time(7), note_at(alto, 7, N, _), N != g, N != b, N != d.

% --- Constraint 9: Final resolution at time 8 ---
note_at(soprano, 8, c, 5).
note_at(alto, 8, c, 4).

% --- Output ---
#show note_at/4.
#show harmonic_interval/2.