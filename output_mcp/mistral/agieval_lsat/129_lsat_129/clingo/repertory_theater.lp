% Domains
movie(horror; mystery; romance; "sci-fi"; western).
screen(1; 2; 3).
time("7pm"; "8pm"; "9pm").

% Time ordering (earlier time before later time)
time_before("7pm", "8pm").
time_before("7pm", "9pm").
time_before("8pm", "9pm").

% Each movie shown exactly once
1 { assigned(M, S, T) : screen(S), time(T) } 1 :- movie(M).

% Screen 3 only shows at 8pm
:- assigned(M, 3, T), T != "8pm".

% Screen 1 and 2 show at 7pm and 9pm only
:- assigned(M, 1, T), T != "7pm", T != "9pm".
:- assigned(M, 2, T), T != "7pm", T != "9pm".

% Sci-fi not on screen 3
:- assigned("sci-fi", 3, _).

% Romance not on screen 2
:- assigned(romance, 2, _).

% Horror and mystery on different screens
:- assigned(horror, S, _), assigned(mystery, S, _).

% Western before horror
:- assigned(western, _, T_w), assigned(horror, _, T_h), time_before(T_h, T_w).

% Define screen 2 movies at specific times
screen2_7pm(M) :- assigned(M, 2, "7pm").
screen2_9pm(M) :- assigned(M, 2, "9pm").

% Ensure that if western is at 9pm, horror cannot be scheduled (impossible)
:- screen2_9pm(western), assigned(horror, _, _).

% Option A: sci-fi at 7pm, horror at 9pm on screen 2
% This is possible if sci-fi is at 7pm, horror at 9pm, and western is before horror (e.g., at 7pm on another screen)
option(a) :- screen2_7pm("sci-fi"), screen2_9pm(horror).

% Option B: sci-fi at 7pm, mystery at 9pm on screen 2
% This is possible if sci-fi is at 7pm, mystery at 9pm, and horror is on another screen before mystery
option(b) :- screen2_7pm("sci-fi"), screen2_9pm(mystery).

% Option C: sci-fi at 7pm, western at 9pm on screen 2
% This is impossible because western must be before horror, and horror must be after western.
% If western is at 9pm, horror must be after 9pm, which is impossible.
% Thus, option(c) should never be derivable.
option(c) :- screen2_7pm("sci-fi"), screen2_9pm(western).

% Option D: western at 7pm, horror at 9pm on screen 2
% This is possible if western is at 7pm, horror at 9pm, and sci-fi is on another screen
option(d) :- screen2_7pm(western), screen2_9pm(horror).

% Option E: western at 7pm, mystery at 9pm on screen 2
% This is possible if western is at 7pm, mystery at 9pm, and horror is on another screen before mystery
option(e) :- screen2_7pm(western), screen2_9pm(mystery).

#show option/1.