% Define domains
client(image; solide; truvest).
channel(website; voicemail).
target(1..3).

% Assign targets - each client-channel pair gets exactly one target
{ target(C, Ch, T) : target(T) } = 1 :- client(C), channel(Ch).

% Constraint 1: website target <= voicemail target for each client
:- client(C), target(C, website, Tw), target(C, voicemail, Tv), Tw > Tv.

% Constraint 2: Image's voicemail target is shorter than others' voicemail targets
:- target(image, voicemail, Ti_v), target(solide, voicemail, Ts_v), Ti_v >= Ts_v.
:- target(image, voicemail, Ti_v), target(truvest, voicemail, Tv_v), Ti_v >= Tv_v.

% Constraint 3: Solide's website target is shorter than Truvest's website target
:- target(solide, website, Ts_w), target(truvest, website, Tv_w), Ts_w >= Tv_w.

% Given: Truvest's website target is shorter than its voicemail target
:- target(truvest, website, Tv_w), target(truvest, voicemail, Tv_v), Tv_w >= Tv_v.

% Map answer choices to conditions
% (A) Image's voicemail target is 2 days.
option(a) :- target(image, voicemail, 2).

% (B) Image's website target is 2 days.
option(b) :- target(image, website, 2).

% (C) Image's website target is 1 day.
option(c) :- target(image, website, 1).

% (D) Solide's website target is 2 days.
option(d) :- target(solide, website, 2).

% (E) Solide's website target is 1 day.
option(e) :- target(solide, website, 1).

#show option/1.