% Domain: C major scale notes
note(c). note(d). note(e). note(f). note(g). note(a). note(b).

% Positions 1-8
position(1..8).

% Semitone values for each note (C=0, D=2, E=4, F=5, G=7, A=9, B=11)
semitone(c, 0).
semitone(d, 2).
semitone(e, 4).
semitone(f, 5).
semitone(g, 7).
semitone(a, 9).
semitone(b, 11).

% Assign exactly one note to each position
1 { melody(P, N) : note(N) } 1 :- position(P).

% Constraint 1: All notes must be from C major scale (already enforced by domain)
% Constraint 2: Start on C (position 1)
melody(1, c).

% Constraint 2: End on C (position 8)
melody(8, c).

% Calculate intervals between consecutive notes
interval(P, S) :- position(P), P < 8, 
                  melody(P, N1), melody(P+1, N2),
                  semitone(N1, S1), semitone(N2, S2),
                  S = S2 - S1.

% Constraint 3: No large leaps greater than 4 semitones
:- interval(P, S), S > 4.
:- interval(P, S), S < -4.

% Calculate absolute interval values for analysis
abs_interval(P, AbsS) :- interval(P, S), AbsS = |S|.

% Determine direction of movement
direction(P, up) :- interval(P, S), S > 0.
direction(P, down) :- interval(P, S), S < 0.
direction(P, same) :- interval(P, S), S = 0.

% Count leaps (intervals larger than 2 semitones)
leap(P) :- abs_interval(P, S), S > 2.

% Count direction changes
direction_change(P) :- position(P), P > 1, P < 8,
                       direction(P-1, D1), direction(P, D2),
                       D1 != D2, D1 != same, D2 != same.

% Analysis predicates
analysis_key("C_major").
analysis_total_steps(8).
final_resolution :- melody(8, c).

% Count leaps
analysis_leap_count(N) :- N = #count{P : leap(P)}.

% Count direction changes
analysis_direction_changes(N) :- N = #count{P : direction_change(P)}.

% Output formatting
#show melody/2.
#show interval/2.
#show analysis_key/1.
#show analysis_total_steps/1.
#show analysis_leap_count/1.
#show analysis_direction_changes/1.
#show final_resolution/0.