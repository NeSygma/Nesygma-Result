% --- Domain ---
note("c", 0).
note("d", 2).
note("e", 4).
note("f", 5).
note("g", 7).
note("a", 9).
note("b", 11).
note("c_oct", 12).

% --- Melody Structure ---
time(1..8).

% --- Choice Rule ---
% Each position must have exactly one note from the scale
1 { melody(T, Name, Pitch) : note(Name, Pitch) } 1 :- time(T).

% --- Constraints ---
% 1. Start and end on tonic (C)
:- melody(1, Name, _), Name != "c".
:- melody(8, Name, _), Name != "c".

% 2. No large leaps greater than 4 semitones
% Interval = abs(Pitch(T+1) - Pitch(T))
:- time(T), T < 8,
   melody(T, _, P1),
   melody(T+1, _, P2),
   Diff = |P1 - P2|,
   Diff > 4.

% --- Analysis ---
% Leap count: intervals > 2 semitones
is_leap(T) :- time(T), T < 8,
              melody(T, _, P1),
              melody(T+1, _, P2),
              |P1 - P2| > 2.

analysis_leap_count(N) :- N = #count { T : is_leap(T) }.

% Direction changes
% Direction at T: 1 (up), -1 (down), 0 (same)
direction(T, 1) :- time(T), T < 8, melody(T, _, P1), melody(T+1, _, P2), P2 > P1.
direction(T, -1) :- time(T), T < 8, melody(T, _, P1), melody(T+1, _, P2), P2 < P1.
direction(T, 0) :- time(T), T < 8, melody(T, _, P1), melody(T+1, _, P2), P2 == P1.

direction_change(T) :- time(T), T < 7,
                       direction(T, D1),
                       direction(T+1, D2),
                       D1 != 0, D2 != 0, D1 != D2.

analysis_direction_changes(N) :- N = #count { T : direction_change(T) }.

% Final resolution
analysis_final_resolution(true) :- melody(8, "c", _).

% --- Output ---
#show melody/2.
#show analysis_leap_count/1.
#show analysis_direction_changes/1.
#show analysis_final_resolution/1.