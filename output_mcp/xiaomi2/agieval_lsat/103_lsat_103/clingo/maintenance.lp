% Domains
client(image). client(solide). client(truvest).
type(website). type(voicemail).
value(1). value(2). value(3).

% Assign targets: exactly one value per client and type
{ target(C, T, V) : value(V) } 1 :- client(C), type(T).

% Constraint 1: Website target cannot be longer than voicemail target
:- target(C, website, V1), target(C, voicemail, V2), V1 > V2.

% Constraint 2: Image's voicemail target is shorter than the others'
:- target(image, voicemail, V1), target(C, voicemail, V2), C != image, V1 >= V2.

% Constraint 3: Solide's website target is shorter than Truvest's
:- target(solide, website, V1), target(truvest, website, V2), V1 >= V2.

% Additional condition: No voicemail target is 3 days
:- target(_, voicemail, 3).

% Check which answer choices hold in each model
holds_a :- target(image, website, 1).
holds_b :- target(solide, website, 2).
holds_c :- target(solide, voicemail, 2).
holds_d :- target(truvest, website, 2).
holds_e :- target(truvest, voicemail, 2).

% The question asks: which does NOT have to be true?
% An option does NOT have to be true if there exists a valid model where it is false.
% We find options that CAN be false (i.e., not holding in some model).

can_be_false_a :- not holds_a.
can_be_false_b :- not holds_b.
can_be_false_c :- not holds_c.
can_be_false_d :- not holds_d.
can_be_false_e :- not holds_e.

% Map to options
option(a) :- can_be_false_a.
option(b) :- can_be_false_b.
option(c) :- can_be_false_c.
option(d) :- can_be_false_d.
option(e) :- can_be_false_e.

#show option/1.
#show target/3.