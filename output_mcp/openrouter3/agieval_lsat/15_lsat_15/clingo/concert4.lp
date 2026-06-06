% Compositions
composition(f). composition(h). composition(l). composition(o). composition(p). composition(r). composition(s). composition(t).

% Time positions 1 through 8
time(1..8).

% Position of each composition (exactly one per time)
1 { position(C, T) : composition(C) } 1 :- time(T).
1 { position(C, T) : time(T) } 1 :- composition(C).

% Helper: composition at position
at(C, T) :- position(C, T).

% Condition 1: T is performed either immediately before F or immediately after R
% T immediately before F: T at time T, F at time T+1
% T immediately after R: R at time T, T at time T+1
condition1 :- at(t, T), at(f, T+1), time(T), time(T+1).
condition1 :- at(r, T), at(t, T+1), time(T), time(T+1).
:- not condition1.

% Condition 2: At least two compositions are performed either after F and before R, or after R and before F
% Count compositions between F and R in either order
count_between_fr(N) :- N = #count{C : at(C, T), at(f, F), at(r, R), F < T, T < R}.
count_between_rf(N) :- N = #count{C : at(C, T), at(r, R), at(f, F), R < T, T < F}.
:- count_between_fr(N), N < 2, count_between_rf(M), M < 2.

% Condition 3: O is performed either first or fifth
condition3 :- at(o, 1).
condition3 :- at(o, 5).
:- not condition3.

% Condition 4: The eighth composition is either L or H
condition4 :- at(l, 8).
condition4 :- at(h, 8).
:- not condition4.

% Condition 5: P is performed before S
condition5 :- at(p, P), at(s, S), P < S.
:- not condition5.

% Condition 6: At least one composition is performed either after O and before S, or after S and before O
count_between_os(N) :- N = #count{C : at(C, T), at(o, O), at(s, S), O < T, T < S}.
count_between_so(N) :- N = #count{C : at(C, T), at(s, S), at(o, O), S < T, T < O}.
:- count_between_os(N), N < 1, count_between_so(M), M < 1.

% Additional condition: If O is performed immediately after T, then F must be performed at certain positions
% First, define when O is immediately after T
o_immediately_after_t :- at(t, T), at(o, T+1), time(T), time(T+1).

% Now, we need to find which positions for F are forced when O is immediately after T
% Let's find all possible positions for F when O is immediately after T
% We'll use a different approach: find all valid sequences where O is immediately after T
% Then check which positions F can be in

% For each position, check if F can be at that position when O is immediately after T
f_at_1 :- o_immediately_after_t, at(f, 1).
f_at_2 :- o_immediately_after_t, at(f, 2).
f_at_3 :- o_immediately_after_t, at(f, 3).
f_at_4 :- o_immediately_after_t, at(f, 4).
f_at_5 :- o_immediately_after_t, at(f, 5).
f_at_6 :- o_immediately_after_t, at(f, 6).
f_at_7 :- o_immediately_after_t, at(f, 7).
f_at_8 :- o_immediately_after_t, at(f, 8).

% Now, we need to check which option is correct
% We'll check each option by seeing if F can be at positions outside that option when O is immediately after T
% If F can be at positions outside the option, then that option is not forced

% Option A: first or second (positions 1 or 2)
% Check if F can be at position 3,4,5,6,7,8 when O is immediately after T
% If F can be at any of these positions, then A is not forced
option(a) :- o_immediately_after_t, not f_at_3, not f_at_4, not f_at_5, not f_at_6, not f_at_7, not f_at_8.

% Option B: second or third (positions 2 or 3)
% Check if F can be at position 1,4,5,6,7,8 when O is immediately after T
option(b) :- o_immediately_after_t, not f_at_1, not f_at_4, not f_at_5, not f_at_6, not f_at_7, not f_at_8.

% Option C: fourth or sixth (positions 4 or 6)
% Check if F can be at position 1,2,3,5,7,8 when O is immediately after T
option(c) :- o_immediately_after_t, not f_at_1, not f_at_2, not f_at_3, not f_at_5, not f_at_7, not f_at_8.

% Option D: fourth or seventh (positions 4 or 7)
% Check if F can be at position 1,2,3,5,6,8 when O is immediately after T
option(d) :- o_immediately_after_t, not f_at_1, not f_at_2, not f_at_3, not f_at_5, not f_at_6, not f_at_8.

% Option E: sixth or seventh (positions 6 or 7)
% Check if F can be at position 1,2,3,4,5,8 when O is immediately after T
option(e) :- o_immediately_after_t, not f_at_1, not f_at_2, not f_at_3, not f_at_4, not f_at_5, not f_at_8.

#show option/1.