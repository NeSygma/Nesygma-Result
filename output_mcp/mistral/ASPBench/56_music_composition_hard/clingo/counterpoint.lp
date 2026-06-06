% Define the domain
% Time steps
{ time(1..8) }.

% Voices
voice(soprano).
voice(alto).

% Notes in C Major
note(c; d; e; f; g; a; b).

% Octaves (MIDI reference)
octave(3; 4; 5).

% Allowed harmonic intervals (in semitones)
harmonic_interval(3; 4; 7; 8; 9; 12; 15; 16).

% Perfect fifth and octave for parallel motion detection
perfect_fifth(7).
octave_interval(12).

% MIDI mappings for notes in different octaves
% C Major scale notes: C, D, E, F, G, A, B
midi_map(c, 3, 48).  % C3
midi_map(c, 4, 60).  % C4
midi_map(c, 5, 72).  % C5

midi_map(d, 3, 50).  % D3
midi_map(d, 4, 62).  % D4
midi_map(d, 5, 74).  % D5

midi_map(e, 3, 52).  % E3
midi_map(e, 4, 64).  % E4
midi_map(e, 5, 76).  % E5

midi_map(f, 3, 53).  % F3
midi_map(f, 4, 65).  % F4
midi_map(f, 5, 77).  % F5

midi_map(g, 3, 55).  % G3
midi_map(g, 4, 67).  % G4
midi_map(g, 5, 79).  % G5

midi_map(a, 3, 57).  % A3
midi_map(a, 4, 69).  % A4
midi_map(a, 5, 81).  % A5

midi_map(b, 3, 59).  % B3
midi_map(b, 4, 71).  % B4
midi_map(b, 5, 83).  % B5

% Voice ranges (MIDI values)
% Soprano: C4 to A5 (MIDI 60-81)
% Alto: E3 to C5 (MIDI 52-72)

% Choice rules for note selection at each time step
% We need to select exactly one note for each voice at each time step
{ soprano_note(T, N, O) : note(N), octave(O) } 1 :- time(T).
{ alto_note(T, N, O) : note(N), octave(O) } 1 :- time(T).

% Convert note+octave to MIDI for easier interval calculations
soprano_midi(T, M) :-
    soprano_note(T, N, O),
    midi_map(N, O, M).

alto_midi(T, M) :-
    alto_note(T, N, O),
    midi_map(N, O, M).

% Calculate harmonic interval at each time step
harmonic_interval(T, I) :-
    time(T),
    soprano_midi(T, SM),
    alto_midi(T, AM),
    I = SM - AM,
    harmonic_interval(I).

% Constraint: Voice ranges
% Soprano: C4-A5 (MIDI 60-81)
:- soprano_midi(T, M), M < 60.
:- soprano_midi(T, M), M > 81.

% Alto: E3-C5 (MIDI 52-72)
:- alto_midi(T, M), M < 52.
:- alto_midi(T, M), M > 72.

% Constraint: No voice crossing (Soprano must be strictly higher than Alto)
:- soprano_midi(T, SM), alto_midi(T, AM), SM =< AM.

% Constraint: Starting notes at time 1
% Alto must be on C4 (MIDI 60)
:- alto_midi(1, M), M != 60.

% Soprano must be on E4 (MIDI 64) or G4 (MIDI 67)
:- soprano_midi(1, M), M != 64, M != 67.

% Constraint: Cadence at time 7 (both notes in V-chord: G, B, D)
% V-chord notes in C Major context: G4(67), B4(71), D5(74) for soprano; G3(55), B3(59), D4(62) for alto
:- time(7),
   soprano_midi(7, SM),
   alto_midi(7, AM),
   not (SM = 67 ; SM = 71 ; SM = 74),
   not (AM = 55 ; AM = 59 ; AM = 62).

% Constraint: Final resolution at time 8
% Soprano on C5 (MIDI 72), Alto on C4 (MIDI 60)
:- soprano_midi(8, M), M != 72.
:- alto_midi(8, M), M != 60.

% Constraint: Melodic leaps in each voice must not exceed perfect fifth (7 semitones)
% For soprano
:- time(T), T < 8,
   soprano_midi(T, M1),
   soprano_midi(T+1, M2),
   abs(M2 - M1) > 7.

% For alto
:- time(T), T < 8,
   alto_midi(T, M1),
   alto_midi(T+1, M2),
   abs(M2 - M1) > 7.

% Helper predicate for parallel motion
same_interval(T, I) :-
    time(T), T < 8,
    soprano_midi(T, SM1), soprano_midi(T+1, SM2),
    alto_midi(T, AM1), alto_midi(T+1, AM2),
    I = SM2 - SM1,
    I = AM2 - AM1.

% Constraint: No parallel perfect fifths
:- time(T), T < 8,
   same_interval(T, I),
   perfect_fifth(I).

% Constraint: No parallel octaves
:- time(T), T < 8,
   same_interval(T, I),
   octave_interval(I).

% Calculate analysis metrics
% Voice crossings (should be 0)
voice_crossing(T) :- soprano_midi(T, SM), alto_midi(T, AM), SM =< AM.

% Parallel fifths violations (should be 0)
parallel_fifths(T) :- time(T), T < 8,
   same_interval(T, I),
   perfect_fifth(I).

% Parallel octaves violations (should be 0)
parallel_octaves(T) :- time(T), T < 8,
   same_interval(T, I),
   octave_interval(I).

% Cadence type at time 7 (authentic cadence)
cadence_ok(7) :- time(7),
   soprano_midi(7, SM),
   alto_midi(7, AM),
   (SM = 67 ; SM = 71 ; SM = 74),
   (AM = 55 ; AM = 59 ; AM = 62).

% Show the composition
#show soprano_note/3.
#show alto_note/3.
#show harmonic_interval/2.

% Show analysis
#show voice_crossing/1.
#show parallel_fifths/1.
#show parallel_octaves/1.
#show cadence_ok/1.