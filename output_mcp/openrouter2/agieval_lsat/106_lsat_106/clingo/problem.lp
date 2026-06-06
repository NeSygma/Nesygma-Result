% Facts
client(image). client(solide). client(truve).
type(website). type(voicemail).
value(1). value(2). value(3).

% Choice rule: each client-type pair gets exactly one value
{ target(C,T,V) : value(V) } 1 :- client(C), type(T).

% Constraints
% website <= voicemail
:- target(C,website,Vw), target(C,voicemail,Vv), Vw > Vv.

% Image voicemail < Solide voicemail and Truvest voicemail
:- target(image,voicemail,Vi), target(solide,voicemail,Vs), Vi >= Vs.
:- target(image,voicemail,Vi), target(truve,voicemail,Vt), Vi >= Vt.

% Solide website < Truvest website
:- target(solide,website,Vs), target(truve,website,Vt), Vs >= Vt.

% Additional condition: Solide voicemail < Truvest website
:- target(solide,voicemail,Vs), target(truve,website,Vt), Vs >= Vt.

% Option mapping
option(a) :- target(image,website,2).
option(b) :- target(image,voicemail,2).
option(c) :- target(solide,website,2).
option(d) :- target(truve,voicemail,2).
option(e) :- target(truve,website,2).

% Exactly one option
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.