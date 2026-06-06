% Melody Generation in C Major Scale

% --- Domain: C Major Scale Notes and their semitone positions ---
note(c, 0).   % C
note(d, 2).   % D
note(e, 4).   % E
note(f, 5).   % F
note(g, 7).   % G
note(a, 9).   % A
note(b, 11).  % B

% Melody positions (1 to 8)
position(1..8).

% --- Generate the melody ---
% Each position gets exactly one note from C major scale
1 { melody(P, N) : note(N, _) } 1 :- position(P).

% --- Fixed start and end ---
melody(1, c).        % Starting note is C
melody(8, c).        % Ending note is C

% --- Compute semitone intervals between consecutive notes ---
% Get semitone value at each position
semitone_at(P, S) :- melody(P, N), note(N, S).

% Interval between position P and P+1 (absolute semitone difference)
% P goes from 1 to 7
interval(P, D) :- 
    position(P), P < 8,
    semitone_at(P, S1),
    semitone_at(P+1, S2),
    D = |S2 - S1|.

% --- Constraint: No large leaps greater than 4 semitones ---
:- interval(P, D), D > 4.

% --- Leap: interval > 2 semitones ---
leap(P) :- interval(P, D), D > 2.

% --- Count leaps ---
leap_count(N) :- N = #count { P : leap(P) }.

% --- Direction changes ---
% Direction at interval P: 1 = up, -1 = down, 0 = same
direction(P, 1) :- interval(P, D), semitone_at(P, S1), semitone_at(P+1, S2), S2 > S1.
direction(P, -1) :- interval(P, D), semitone_at(P, S1), semitone_at(P+1, S2), S2 < S1.
direction(P, 0) :- interval(P, D), semitone_at(P, S1), semitone_at(P+1, S2), S2 = S1.

% Direction change: direction at P differs from direction at P-1 (P from 2 to 7)
direction_change(P) :- 
    direction(P, D1), direction(P-1, D2), 
    D1 != D2,
    position(P), P < 8.

direction_change_count(N) :- N = #count { P : direction_change(P) }.

% --- Final resolution: melody ends on tonic (C) ---
% Already enforced by melody(8, c)
final_resolution(true) :- melody(8, c).

% --- Derived outputs ---
% analysis.key = C_major
analysis_key("C_major").

% analysis.total_steps = 8
analysis_total_steps(8).

% Show results
#show melody/2.
#show interval/2.
#show leap_count/1.
#show direction_change_count/1.
#show final_resolution/1.
#show analysis_key/1.
#show analysis_total_steps/1.