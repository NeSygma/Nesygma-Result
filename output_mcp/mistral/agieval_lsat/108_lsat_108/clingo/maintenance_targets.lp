% Clients and channels
client(image; solide; truvest).
channel(website; voicemail).
target(1; 2; 3).

% Additional constraint: none of the clients has a website target of 2 days
:- target_set(C, website, 2), client(C).

% Each client has exactly one target per channel
1 { target_set(C, Ch, T) : target(T) } 1 :- client(C), channel(Ch).

% Constraint: website target <= voicemail target for each client
:- target_set(C, website, W), target_set(C, voicemail, V), W > V.

% Constraint: Image's voicemail target < Solide's voicemail target
:- target_set(image, voicemail, V1), target_set(solide, voicemail, V2), V1 >= V2.

% Constraint: Image's voicemail target < Truvest's voicemail target
:- target_set(image, voicemail, V1), target_set(truvest, voicemail, V3), V1 >= V3.

% Constraint: Solide's website target < Truvest's website target
:- target_set(solide, website, W2), target_set(truvest, website, W3), W2 >= W3.

% Define the options
% (A) Image's website target is shorter than Solide's
option(a) :- target_set(image, website, W1),
             target_set(solide, website, W2),
             W1 < W2.

% (B) Solide's website target is shorter than Image's
option(b) :- target_set(solide, website, W2),
             target_set(image, website, W1),
             W2 < W1.

% (C) Solide's voicemail target is shorter than Truvest's
option(c) :- target_set(solide, voicemail, V2),
             target_set(truvest, voicemail, V3),
             V2 < V3.

% (D) Truvest's website target is shorter than Image's
option(d) :- target_set(truvest, website, W3),
             target_set(image, website, W1),
             W3 < W1.

% (E) Truvest's voicemail target is shorter than Solide's
option(e) :- target_set(truvest, voicemail, V3),
             target_set(solide, voicemail, V2),
             V3 < V2.

#show option/1.