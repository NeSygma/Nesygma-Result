% C major scale notes and their semitone positions relative to C
note("C", 0).
note("D", 2).
note("E", 4).
note("F", 5).
note("G", 7).
note("A", 9).
note("B", 11).

% Melody positions (0-indexed)
position(0..7).

% Each position gets exactly one note from the C major scale
1 { melody(P, N) : note(N, _) } 1 :- position(P).

% Starting note must be C
melody(0, "C").

% Ending note must be C
melody(7, "C").

% Calculate semitone intervals between consecutive notes
interval(P, I) :- 
    position(P), P < 7,
    melody(P, N1), note(N1, S1),
    melody(P+1, N2), note(N2, S2),
    I = S2 - S1.

% Constraint: No leap greater than 4 semitones (absolute value)
:- interval(P, I), I > 4.
:- interval(P, I), I < -4.

% Count leaps (intervals larger than 2 semitones in absolute value)
leap(P) :- interval(P, I), I > 2.
leap(P) :- interval(P, I), I < -2.

leap_count(N) :- N = #count { P : leap(P) }.

% Direction changes
% Direction: 1 = up, -1 = down, 0 = same
direction(P, 1) :- interval(P, I), I > 0.
direction(P, -1) :- interval(P, I), I < 0.
direction(P, 0) :- interval(P, I), I = 0.

% A direction change occurs when consecutive intervals have opposite signs
% (one positive, one negative) or one is zero and the other is non-zero
direction_change(P) :- 
    position(P), P < 6,
    direction(P, D1), direction(P+1, D2),
    D1 != 0, D2 != 0, D1 != D2.
direction_change(P) :-
    position(P), P < 6,
    direction(P, 0), direction(P+1, D2), D2 != 0.
direction_change(P) :-
    position(P), P < 6,
    direction(P, D1), D1 != 0, direction(P+1, 0).

direction_change_count(N) :- N = #count { P : direction_change(P) }.

% Final resolution: melody ends on tonic (C)
final_resolution :- melody(7, "C").

% Analysis output
analysis_key("C_major").
analysis_total_steps(8).

% Show results
#show melody/2.
#show interval/2.
#show analysis_key/1.
#show analysis_total_steps/1.
#show leap_count/1.
#show direction_change_count/1.
#show final_resolution/1.