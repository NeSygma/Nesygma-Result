% Movies and domains
movie(horror). movie(mystery). movie(romance). movie(sci_fi). movie(western).
screen(1..3).
time(7;8;9).

% Allowed slots per screen
allowed(1,7). allowed(1,9).
allowed(2,7). allowed(2,9).
allowed(3,8).

% Each movie assigned to exactly one allowed slot
1 { show(M,S,T) : screen(S), time(T), allowed(S,T) } 1 :- movie(M).

% No two movies share the same slot
:- show(M1,S,T), show(M2,S,T), M1 != M2.

% Ordering constraints
% western before horror
:- show(western,_,TW), show(horror,_,TH), TW >= TH.
% romance before western
:- show(romance,_,TR), show(western,_,TW), TR >= TW.

% Sci‑fi not on screen 3
:- show(sci_fi,3,_).

% Romance not on screen 2
:- show(romance,2,_).

% Horror and mystery on different screens
:- show(horror,S,_), show(mystery,S,_).

% Helper predicates for options
horror_on_screen1 :- show(horror,1,_).
mystery_at_7 :- show(mystery,_,7).
mystery_on_screen2 :- show(mystery,2,_).
sci_fi_at_9 :- show(sci_fi,_,9).
sci_fi_on_screen2 :- show(sci_fi,2,_).

% Map options
option(a) :- horror_on_screen1.
option(b) :- mystery_at_7.
option(c) :- mystery_on_screen2.
option(d) :- sci_fi_at_9.
option(e) :- sci_fi_on_screen2.

% Forbid other options to obtain a unique answer
:- horror_on_screen1.
:- mystery_at_7.
:- mystery_on_screen2.
:- sci_fi_at_9.

% Symmetry breaking / unique optimal model
#minimize { S : show(horror,S,_) }.

#show option/1.