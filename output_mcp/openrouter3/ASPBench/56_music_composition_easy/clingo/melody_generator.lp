% Melody Generator in C Major Scale
% Problem: Generate 8-note melody with harmonic rules and voice leading constraints

% ===== DOMAINS =====
% Positions in melody (1-8)
position(1..8).

% Notes in C major scale
note("C"). note("D"). note("E"). note("F"). note("G"). note("A"). note("B").

% Semitone values for each note (C major scale)
semitone("C", 0). semitone("D", 2). semitone("E", 4). semitone("F", 5).
semitone("G", 7). semitone("A", 9). semitone("B", 11).

% ===== MELODY GENERATION =====
% Each position must have exactly one note from the scale
1 { melody(P, N) : note(N) } 1 :- position(P).

% ===== CONSTRAINTS =====
% 1. Start and end on tonic (C)
melody(1, "C").
melody(8, "C").

% 2. No large leaps greater than 4 semitones
% Calculate interval between consecutive notes
interval(P, Diff) :- 
    position(P), P < 8,
    melody(P, N1), melody(P+1, N2),
    semitone(N1, S1), semitone(N2, S2),
    Diff = S2 - S1.

% Forbidden: intervals > 4 semitones
:- interval(P, Diff), Diff > 4.
:- interval(P, Diff), Diff < -4.

% ===== ANALYSIS =====
% Key is always C major
analysis("key", "C_major").

% Total steps (notes)
analysis("total_steps", 8).

% Leap count: intervals larger than 2 semitones (absolute value)
leap(P) :- interval(P, Diff), Diff > 2.
leap(P) :- interval(P, Diff), Diff < -2.
analysis("leap_count", N) :- N = #count{P : leap(P)}.

% Direction changes: when interval sign changes
% First, determine direction at each interval
direction(P, "up") :- interval(P, Diff), Diff > 0.
direction(P, "down") :- interval(P, Diff), Diff < 0.
direction(P, "same") :- interval(P, 0).

% Direction change occurs when direction differs from previous
direction_change(P) :- 
    position(P), P > 1, P < 8,
    direction(P, D1), direction(P-1, D2), D1 != D2.

analysis("direction_changes", N) :- N = #count{P : direction_change(P)}.

% Final resolution: ends on tonic (C)
analysis("final_resolution", true) :- melody(8, "C").

% ===== SHOW DIRECTIVES =====
#show melody/2.
#show interval/3.
#show analysis/2.
#show leap/1.
#show direction_change/1.