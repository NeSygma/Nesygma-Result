% Domain: C major scale notes
note(c; d; e; f; g; a; b).

% Melody positions (0 to 7)
position(0..7).

% Define semitone values for each note in C major
semitone(c, 0).
semitone(d, 2).
semitone(e, 4).
semitone(f, 5).
semitone(g, 7).
semitone(a, 9).
semitone(b, 11).

% Melody: assign a note to each position
1 { melody(P, N) : note(N) } 1 :- position(P).

% Start and end on C
:- not melody(0, c).
:- not melody(7, c).

% Calculate intervals between consecutive notes (semitone differences)
interval(P, I) :-
    position(P), P < 7,
    melody(P, N1), melody(P+1, N2),
    semitone(N1, S1), semitone(N2, S2),
    I = S2 - S1.

% No large leaps > 4 semitones (both up and down)
:- interval(P, I), I > 4.
:- interval(P, I), I < -4.

% Analysis: key is always C major
analysis_key("C_major").

% Analysis: total steps = 8
analysis_total_steps(8).

% Analysis: leap_count = count of intervals > 2 semitones (absolute value)
leap(P) :- interval(P, I), I > 2.
leap(P) :- interval(P, I), I < -2.
analysis_leap_count(L) :- L = #count{ P : leap(P) }.

% Analysis: direction_changes
% Direction of each interval: +1 for ascending, -1 for descending, 0 for same
interval_direction(P, 1) :- interval(P, I), I > 0.
interval_direction(P, -1) :- interval(P, I), I < 0.
interval_direction(P, 0) :- interval(P, 0).

% Direction change occurs when consecutive intervals have different non-zero directions
direction_change(P) :-
    position(P), P > 0, P < 7,
    interval_direction(P-1, D1), interval_direction(P, D2),
    D1 != 0, D2 != 0, D1 != D2.

analysis_direction_changes(C) :- C = #count{ P : direction_change(P) }.

% Analysis: final_resolution = true if ends on tonic (C)
analysis_final_resolution(true) :- melody(7, c).
analysis_final_resolution(false) :- melody(7, N), N != c.

% Show the results
#show melody/2.
#show analysis_key/1.
#show analysis_total_steps/1.
#show analysis_leap_count/1.
#show analysis_direction_changes/1.
#show analysis_final_resolution/1.