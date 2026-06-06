% Domains and possible targets
target(1..3).
client(image; solide; truvest).
channel(website; voicemail).

% Service targets are assigned to each client-channel pair
% We represent this as target(C, Ch, T) where C is client, Ch is channel, T is target value.
% Since the problem states two targets per client (one for website, one for voicemail),
% we will assign exactly one target per client-channel pair.

% Choice rule: Assign a target to each client-channel pair
{ target(C, Ch, T) : target(T) } = 1 :- client(C), channel(Ch).

% Constraints from the problem:

% 1. None of the clients can have a website target that is longer than its voicemail target.
%    This means for each client, the website target must be <= voicemail target.
:- client(C), target(C, website, T1), target(C, voicemail, T2), T1 > T2.

% 2. Image's voicemail target must be shorter than the other clients' voicemail targets.
%    This means Image's voicemail target < Solide's voicemail target AND Image's voicemail target < Truvest's voicemail target.
:- client(C), C != image, target(image, voicemail, T1), target(C, voicemail, T2), T1 >= T2.

% 3. Solide's website target must be shorter than Truvest's website target.
:- target(solide, website, T1), target(truvest, website, T2), T1 >= T2.

% Given condition: Image's website target is 2 days.
target(image, website, 2).

% Now, we need to determine which of the following must also be 2 days:
% (A) Image's voicemail target
% (B) Solide's website target
% (C) Solide's voicemail target
% (D) Truvest's website target
% (E) Truvest's voicemail target

% Let's derive the necessary conditions for each option to be 2 days.

% (A) Image's voicemail target must be 2 days
% From constraint 2, Image's voicemail target must be shorter than Solide's and Truvest's voicemail targets.
% If Image's voicemail target is 2, then Solide's and Truvest's voicemail targets must be > 2, i.e., 3.
% Also, from constraint 1, Image's website target (2) <= Image's voicemail target.
% So Image's voicemail target can be 2 or 3.
% But if it is 3, then Solide's and Truvest's voicemail targets must be > 3, which is impossible (max target is 3).
% Therefore, Image's voicemail target must be 2.
answer(a) :- target(image, voicemail, 2).

% (B) Solide's website target must be 2 days
% From constraint 3, Solide's website target < Truvest's website target.
% If Solide's website target is 2, then Truvest's website target must be 3.
% But there is no constraint forcing Solide's website target to be 2.
% It could be 1 or 2.
% So this is not necessarily true.
answer(b) :- target(solide, website, 2).

% (C) Solide's voicemail target must be 2 days
% From constraint 2, Image's voicemail target < Solide's voicemail target.
% If Image's voicemail target is 2, then Solide's voicemail target must be > 2, i.e., 3.
% So Solide's voicemail target cannot be 2.
answer(c) :- target(solide, voicemail, 2).

% (D) Truvest's website target must be 2 days
% From constraint 3, Solide's website target < Truvest's website target.
% If Solide's website target is 1, Truvest's website target could be 2 or 3.
% If Solide's website target is 2, Truvest's website target must be 3.
% So Truvest's website target is not necessarily 2.
answer(d) :- target(truvest, website, 2).

% (E) Truvest's voicemail target must be 2 days
% From constraint 2, Image's voicemail target < Truvest's voicemail target.
% If Image's voicemail target is 2, then Truvest's voicemail target must be > 2, i.e., 3.
% So Truvest's voicemail target cannot be 2.
answer(e) :- target(truvest, voicemail, 2).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- answer(a).
option(b) :- answer(b).
option(c) :- answer(c).
option(d) :- answer(d).
option(e) :- answer(e).

#show option/1.