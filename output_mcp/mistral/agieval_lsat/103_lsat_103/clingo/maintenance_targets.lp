% Domain
client(image; solide; truvest).
channel(website; voicemail).
target(1; 2; 3).

% Assign targets to each client-channel pair
1 { target(C, Ch, T) : target(T) } 1 :- client(C), channel(Ch).

% Constraint 1: Website target <= Voicemail target for each client
:- target(C, website, T1), target(C, voicemail, T2), T1 > T2.

% Constraint 2: Image's voicemail target < other clients' voicemail targets
:- target(image, voicemail, T), target(solide, voicemail, T2), T >= T2.
:- target(image, voicemail, T), target(truvest, voicemail, T3), T >= T3.

% Constraint 3: Solide's website target < Truvest's website target
:- target(solide, website, T1), target(truvest, website, T2), T1 >= T2.

% Condition: No client has a voicemail target of 3 days
:- target(C, voicemail, 3).

% Define conditions for each option
% Option A: Image's website target is 1 day
option_a :- target(image, website, 1).
% Option B: Solide's website target is 2 days
option_b :- target(solide, website, 2).
% Option C: Solide's voicemail target is 2 days
option_c :- target(solide, voicemail, 2).
% Option D: Truvest's website target is 2 days
option_d :- target(truvest, website, 2).
% Option E: Truvest's voicemail target is 2 days
option_e :- target(truvest, voicemail, 2).

% The correct answer is the option that is NOT true in the model
% So we need to find which option is false while the others are true
answer(b) :- not option_b, option_a, option_c, option_d, option_e.

% Show the answer
#show answer/1.