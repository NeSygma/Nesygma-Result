% ============================================
% 8-Note Melody Generator in C Major Scale
% ============================================

% --- Domain: Notes in C major scale ---
note(c). note(d). note(e). note(f). note(g). note(a). note(b).

% --- Semitone values for each note (relative to C) ---
semitone(c, 0).
semitone(d, 2).
semitone(e, 4).
semitone(f, 5).
semitone(g, 7).
semitone(a, 9).
semitone(b, 11).

% --- Positions 1 through 8 ---
position(1..8).

% --- Interval positions 1 through 7 (between consecutive notes) ---
interval_pos(1..7).

% ============================================
% CHOICE: Assign a note to each position
% ============================================
1 { melody(P, N) : note(N) } 1 :- position(P).

% ============================================
% CONSTRAINTS
% ============================================

% Constraint 1: Start on C (tonic)
:- not melody(1, c).

% Constraint 2: End on C (tonic)
:- not melody(8, c).

% Constraint 3: No large leaps greater than 4 semitones
% Calculate absolute interval between consecutive notes
interval(P, Diff) :- interval_pos(P), 
                     melody(P, N1), melody(P+1, N2),
                     semitone(N1, S1), semitone(N2, S2),
                     Diff = |S1 - S2|.

% Forbid intervals larger than 4 semitones
:- interval_pos(P), interval(P, Diff), Diff > 4.

% ============================================
% ANALYSIS METRICS
% ============================================

% Leap count: intervals larger than 2 semitones
leap(P) :- interval_pos(P), interval(P, Diff), Diff > 2.
leap_count(N) :- N = #count { P : leap(P) }.

% Direction of each interval: up(1), down(-1), same(0)
direction(P, 1) :- interval_pos(P), 
                   melody(P, N1), melody(P+1, N2),
                   semitone(N1, S1), semitone(N2, S2),
                   S2 > S1.
direction(P, -1) :- interval_pos(P), 
                    melody(P, N1), melody(P+1, N2),
                    semitone(N1, S1), semitone(N2, S2),
                    S2 < S1.
direction(P, 0) :- interval_pos(P), 
                   melody(P, N1), melody(P+1, N2),
                   semitone(N1, S1), semitone(N2, S2),
                   S2 == S1.

% Direction changes: when direction differs from previous
direction_change(P) :- interval_pos(P), P > 1,
                       direction(P, D1), direction(P-1, D2),
                       D1 != D2.
direction_changes(N) :- N = #count { P : direction_change(P) }.

% Final resolution: melody ends on tonic (C)
final_resolution :- melody(8, c).

% ============================================
% OUTPUT: Show the melody and analysis
% ============================================

#show melody/2.
#show interval/2.
#show leap_count/1.
#show direction_changes/1.
#show final_resolution/0.