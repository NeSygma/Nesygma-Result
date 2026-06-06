% Clients and channels
client(image; solide; truvest).
channel(website; voicemail).
target(1; 2; 3).

% Assign targets to each client-channel pair
{ target(C, Ch, T) : target(T) } = 1 :- client(C), channel(Ch).

% Constraint 1: For each client, website target <= voicemail target
:- client(C), target(C, website, T1), target(C, voicemail, T2), T1 > T2.

% Constraint 2: Image's voicemail target must be shorter than the other clients' voicemail targets
:- target(image, voicemail, T1), target(solide, voicemail, T2), T1 >= T2.
:- target(image, voicemail, T1), target(truvest, voicemail, T2), T1 >= T2.

% Constraint 3: Solide's website target must be shorter than Truvest's website target
:- target(solide, website, T1), target(truvest, website, T2), T1 >= T2.

% Additional condition: Truvest's website target is shorter than its voicemail target
:- target(truvest, website, T1), target(truvest, voicemail, T2), T1 >= T2.

% Derive the answer choices
% (A) Image's voicemail target is 2 days
option(a) :- target(image, voicemail, 2).

% (B) Image's website target is 2 days
option(b) :- target(image, website, 2).

% (C) Image's website target is 1 day
option(c) :- target(image, website, 1).

% (D) Solide's website target is 2 days
option(d) :- target(solide, website, 2).

% (E) Solide's website target is 1 day
option(e) :- target(solide, website, 1).

#show option/1.