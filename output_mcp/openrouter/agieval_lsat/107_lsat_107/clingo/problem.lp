% Days
day(1). day(2). day(3).
% Clients
client(image). client(solide). client(truvest).
% Channels
channel(website). channel(voicemail).

% Assign exactly one target per client per channel
{ target(C, website, D) : day(D) } = 1 :- client(C).
{ target(C, voicemail, D) : day(D) } = 1 :- client(C).

% Constraints
% 1. website target not longer than voicemail target for each client
:- target(C, website, Dw), target(C, voicemail, Dv), Dw > Dv.
% 2. Image's voicemail target shorter than others' voicemail targets
:- target(image, voicemail, Di), client(Other), Other != image, target(Other, voicemail, Do), Di >= Do.
% 3. Solide's website target shorter than Truvest's website target
:- target(solide, website, Ds), target(truvest, website, Dt), Ds >= Dt.

% Count predicates for each option
cnt_a(N) :- N = #count { C : target(C, website, 1) }.
cnt_b(N) :- N = #count { C : target(C, voicemail, 2) }.
cnt_c(N) :- N = #count { C : target(C, website, 2) }.
cnt_d(N) :- N = #count { C : target(C, voicemail, 3) }.
cnt_e(N) :- N = #count { C : target(C, website, 3) }.

% Helper predicates for >=2
ge2_a :- cnt_a(N), N >= 2.
ge2_b :- cnt_b(N), N >= 2.
ge2_c :- cnt_c(N), N >= 2.
ge2_d :- cnt_d(N), N >= 2.
ge2_e :- cnt_e(N), N >= 2.

% Test flags and impossibility detection
{ test_a }. { test_b }. { test_c }. { test_d }. { test_e }.
% Ensure exactly one test is considered (optional, but we allow multiple)
% If a test is selected, enforce that the corresponding count is >=2
:- test_a, not ge2_a.
:- test_b, not ge2_b.
:- test_c, not ge2_c.
:- test_d, not ge2_d.
:- test_e, not ge2_e.

% Impossibility derivation via loop
impossible_a :- not test_a.
impossible_b :- not test_b.
impossible_c :- not test_c.
impossible_d :- not test_d.
impossible_e :- not test_e.

test_a :- not impossible_a.
test_b :- not impossible_b.
test_c :- not impossible_c.
test_d :- not impossible_d.
test_e :- not impossible_e.

% Map answer: option X if impossible_X holds
option(a) :- impossible_a.
option(b) :- impossible_b.
option(c) :- impossible_c.
option(d) :- impossible_d.
option(e) :- impossible_e.

#show option/1.