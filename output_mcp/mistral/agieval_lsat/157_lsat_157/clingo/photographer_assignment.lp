% Domains
photographer(frost; gonzalez; heideck; knutson; lai; mays).
ceremony(silva; thorne).

% Assignment: each photographer can be assigned to at most one ceremony (0 or 1)
{ assigned(P, C) : ceremony(C) } 0..1 :- photographer(P).

% At least two photographers per ceremony
:- ceremony(C), #count{P: assigned(P, C)} < 2.

% Frost must be assigned together with Heideck to one ceremony
frost_heideck_together :- assigned(frost, C), assigned(heideck, C).
:- not frost_heideck_together.

% If Lai and Mays are both assigned, they must be to different ceremonies
:- assigned(lai, C), assigned(mays, C).

% If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
:- not assigned(knutson, thorne), not assigned(heideck, thorne).
:- not assigned(knutson, thorne), not assigned(mays, thorne).

% Define what it means for each option to be the complete Silva assignment
silva_option_a :- assigned(frost, silva), assigned(gonzalez, silva), assigned(heideck, silva), assigned(knutson, silva),
                  not assigned(lai, silva), not assigned(mays, silva).

silva_option_b :- assigned(frost, silva), assigned(gonzalez, silva), assigned(heideck, silva),
                  not assigned(knutson, silva), not assigned(lai, silva), not assigned(mays, silva).

silva_option_c :- assigned(gonzalez, silva), assigned(knutson, silva),
                  not assigned(frost, silva), not assigned(heideck, silva), not assigned(lai, silva), not assigned(mays, silva).

silva_option_d :- assigned(heideck, silva), assigned(lai, silva),
                  not assigned(frost, silva), not assigned(gonzalez, silva), not assigned(knutson, silva), not assigned(mays, silva).

silva_option_e :- assigned(knutson, silva), assigned(mays, silva),
                  not assigned(frost, silva), not assigned(gonzalez, silva), not assigned(heideck, silva), not assigned(lai, silva).

% Map to answer choices
option(a) :- silva_option_a.
option(b) :- silva_option_b.
option(c) :- silva_option_c.
option(d) :- silva_option_d.
option(e) :- silva_option_e.

#show option/1.