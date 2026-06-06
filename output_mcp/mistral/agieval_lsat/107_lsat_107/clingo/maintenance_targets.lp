% Define clients, channels, and targets
client(image).
client(solide).
client(truvest).

channel(website).
channel(voicemail).

target(1).
target(2).
target(3).

% For each client and channel, assign a target
{ target(C, Ch, T) : target(T) } 1 :- client(C), channel(Ch).

% Constraint 1: For each client, website target <= voicemail target
:- client(C), target(C, website, T1), target(C, voicemail, T2), T1 > T2.

% Constraint 2: Image's voicemail target must be shorter than the other clients' voicemail targets
:- target(image, voicemail, T1), target(solide, voicemail, T2), T1 >= T2.
:- target(image, voicemail, T1), target(truvest, voicemail, T2), T1 >= T2.

% Constraint 3: Solide's website target must be shorter than Truvest's website target
:- target(solide, website, T1), target(truvest, website, T2), T1 >= T2.

% Define predicates for each option being set for more than one client
two_clients_1d_website :- client(C1), client(C2), C1 != C2, target(C1, website, 1), target(C2, website, 1).
two_clients_2d_voicemail :- client(C1), client(C2), C1 != C2, target(C1, voicemail, 2), target(C2, voicemail, 2).
two_clients_2d_website :- client(C1), client(C2), C1 != C2, target(C1, website, 2), target(C2, website, 2).
two_clients_3d_voicemail :- client(C1), client(C2), C1 != C2, target(C1, voicemail, 3), target(C2, voicemail, 3).
two_clients_3d_website :- client(C1), client(C2), C1 != C2, target(C1, website, 3), target(C2, website, 3).

% The correct answer is the option for which two_clients_* is impossible
% We use the fact that if two_clients_* is impossible, the corresponding option must be the answer
answer(e) :- not two_clients_3d_website.
answer(d) :- not answer(e), not two_clients_3d_voicemail.
answer(c) :- not answer(e), not answer(d), not two_clients_2d_website.
answer(b) :- not answer(e), not answer(d), not answer(c), not two_clients_2d_voicemail.
answer(a) :- not answer(e), not answer(d), not answer(c), not answer(b), not two_clients_1d_website.

% Map the correct answer to option/1
option(X) :- answer(X).

#show option/1.