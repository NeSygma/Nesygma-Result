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

% An option MUST be true if it holds in ALL valid models.
% An option does NOT have to be true if there exists a model where it's false.
% We want the option that does NOT have to be true (can be false).

% We need to find which option can be false.
% Use a meta-approach: for each option, check if it's possible to have a model where it's false.

% Show all models with their target assignments and which holds are true/false
#show target/3.
#show holds_a/0.
#show holds_b/0.
#show holds_c/0.
#show holds_d/0.
#show holds_e/0.