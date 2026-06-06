% Clients and days
client(image; solide; truvest).
day(1..3).

% Exactly one website and voicemail target per client
1 { website(C, D) : day(D) } 1 :- client(C).
1 { voicemail(C, D) : day(D) } 1 :- client(C).

% Constraints
% Website target cannot be longer than voicemail target (i.e., larger number)
:- website(C, D1), voicemail(C, D2), D1 > D2.

% Image's voicemail shorter than others
:- voicemail(image, Di), voicemail(solide, Ds), Di >= Ds.
:- voicemail(image, Di), voicemail(truvest, Dt), Di >= Dt.

% Solide's website shorter than Truvest's website
:- website(solide, D1), website(truvest, D2), D1 >= D2.

% Premise: Truvest's website shorter than its voicemail target
:- website(truvest, Wt), voicemail(truvest, Vt), Wt >= Vt.

% Options mapping (only the forced one should appear)
option(a) :- website(image, 2), website(image, 3).
option(b) :- website(image, 2), website(image, 1).
option(c) :- website(image, 1), website(image, 2).
option(d) :- website(solide, 2), website(solide, 3).
option(e) :- website(solide, 1).

#show option/1.