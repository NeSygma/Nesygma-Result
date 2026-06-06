% --- Declare the C major scale notes ---
note(c; d; e; f; g; a; b).

% --- Define semitone differences between notes ---
semitone(c, d, 2).
semitone(c, e, 4).
semitone(c, f, 5).
semitone(c, g, 7).
semitone(c, a, 9).
semitone(c, b, 11).
semitone(d, c, 10).
semitone(d, e, 2).
semitone(d, f, 3).
semitone(d, g, 5).
semitone(d, a, 7).
semitone(d, b, 9).
semitone(e, c, 7).
semitone(e, d, 5).
semitone(e, f, 2).
semitone(e, g, 4).
semitone(e, a, 6).
semitone(e, b, 8).
semitone(f, c, 5).
semitone(f, d, 3).
semitone(f, e, 2).
semitone(f, g, 2).
semitone(f, a, 4).
semitone(f, b, 6).
semitone(g, c, 0).
semitone(g, d, 2).
semitone(g, e, 4).
semitone(g, f, 5).
semitone(g, a, 2).
semitone(g, b, 4).
semitone(a, c, 9).
semitone(a, d, 7).
semitone(a, e, 5).
semitone(a, f, 4).
semitone(a, g, 2).
semitone(a, b, 2).
semitone(b, c, 1).
semitone(b, d, 3).
semitone(b, e, 5).
semitone(b, f, 7).
semitone(b, g, 9).
semitone(b, a, 11).

% --- Define positions ---
position(1..8).

% --- Generate melody ---
{ melody(P, N) : note(N) } = 1 :- position(P).

% --- Start and end on c ---
:- melody(1, N), N != c.
:- melody(8, N), N != c.

% --- Calculate intervals ---
interval(P, I) :- melody(P, N1), melody(P+1, N2), semitone(N1, N2, I), position(P), P < 8.

% --- Intervals must be <= 4 semitones ---
:- interval(P, I), I > 4, position(P), P < 8.

% --- Calculate leaps (intervals > 2 semitones) ---
leap(P) :- interval(P, I), I > 2, position(P), P < 8.
analysis_leap_count(C) :- C = #count{ P : leap(P) }.

% --- Calculate directions ---
direction(P, ascending) :- interval(P, I1), interval(P+1, I2), I1 < I2, position(P), P < 7.
direction(P, descending) :- interval(P, I1), interval(P+1, I2), I1 > I2, position(P), P < 7.
direction(P, same) :- interval(P, I1), interval(P+1, I2), I1 = I2, position(P), P < 7.

% --- Calculate direction changes ---
direction_change(P) :- direction(P, D1), direction(P+1, D2), D1 != D2, position(P), P < 7.
analysis_direction_changes(C) :- C = #count{ P : direction_change(P) }.

% --- Final resolution (ends on c) ---
analysis_final_resolution :- melody(8, c).

% --- Total steps (always 8) ---
analysis_total_steps(8).

% --- Show the melody and analysis ---
#show melody/2.
#show interval/2.
#show analysis_total_steps/1.
#show analysis_leap_count/1.
#show analysis_direction_changes/1.
#show analysis_final_resolution/0.