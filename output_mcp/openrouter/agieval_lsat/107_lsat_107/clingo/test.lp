% Days
day(1..3).
% Clients
client(image;solide;truvest).
% Channels
channel(website;voicemail).

% Assign exactly one target per client per channel
{ target(C, website, D) : day(D) } = 1 :- client(C).
{ target(C, voicemail, D) : day(D) } = 1 :- client(C).

% Constraints
:- target(C, website, Dw), target(C, voicemail, Dv), Dw > Dv.
:- target(image, voicemail, Di), client(Other), Other != image, target(Other, voicemail, Do), Di >= Do.
:- target(solide, website, Ds), target(truvest, website, Dt), Ds >= Dt.

% detect two clients with website=3
two_clients_website3 :- target(C1, website, 3), target(C2, website, 3), C1 != C2.

#show two_clients_website3/0.