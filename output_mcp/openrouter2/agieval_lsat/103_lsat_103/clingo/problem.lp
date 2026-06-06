% Clients
client(image). client(solide). client(truvest).

% Target types
target_type(website). target_type(voicemail).

% Days
day(1). day(2). day(3).

% Choice rule: each client has exactly one target for each type
1 { target(C, T, D) : day(D) } 1 :- client(C), target_type(T).

% Constraint: no voicemail target is 3
:- target(C, voicemail, 3).

% Constraint: website <= voicemail
:- target(C, website, D1), target(C, voicemail, D2), D1 > D2.

% Constraint: Image's voicemail < Solide's voicemail and < Truvest's voicemail
:- target(image, voicemail, D1), target(solide, voicemail, D2), D1 >= D2.
:- target(image, voicemail, D1), target(truvest, voicemail, D3), D1 >= D3.

% Constraint: Solide's website < Truvest's website
:- target(solide, website, D1), target(truvest, website, D2), D1 >= D2.

% Option mapping
option(a) :- false.
option(b) :- not target(solide, website, 2).
option(c) :- false.
option(d) :- false.
option(e) :- false.

#show option/1.