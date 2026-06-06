% Domain declarations
photographer(frost; gonzalez; heideck; knutson; lai; mays).
university(silva; thorne).

% Base assignment constraints
1 { assigned(P, U) : university(U) } 1 :- photographer(P).
:- university(U), #count{P: assigned(P, U)} < 2.
:- assigned(P, silva), assigned(P, thorne).

% Constraint 1: Frost and Heideck must be assigned together
assigned(frost, U) :- assigned(heideck, U).
assigned(heideck, U) :- assigned(frost, U).

% Constraint 2: Lai and Mays cannot be assigned to the same university
:- assigned(lai, U), assigned(mays, U).

% Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assigned(gonzalez, silva), not assigned(lai, thorne).

% Constraint 4: If Knutson is not assigned to Thorne, then Heideck and Mays must be assigned to Thorne
:- not assigned(knutson, thorne), not assigned(heideck, thorne).
:- not assigned(knutson, thorne), not assigned(mays, thorne).

% Must-assign photographers (derived from constraints)
must_assign(frost).
must_assign(heideck).
must_assign(knutson).

% Map the correct answer to option/1
option(a) :- must_assign(frost), must_assign(heideck), not must_assign(knutson).
option(b) :- must_assign(frost), must_assign(heideck), must_assign(knutson).
option(c) :- must_assign(frost), must_assign(heideck), must_assign(knutson), must_assign(lai).
option(d) :- must_assign(frost), must_assign(gonzalez), must_assign(heideck).
option(e) :- must_assign(frost), must_assign(gonzalez), must_assign(heideck), must_assign(mays).

#show option/1.