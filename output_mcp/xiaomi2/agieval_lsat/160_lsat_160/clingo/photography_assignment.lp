% Domains
ceremony(silva). ceremony(thorne).
photographer(frost). photographer(gonzalez). photographer(heideck). photographer(knutson). photographer(lai). photographer(mays).

% Option identifiers
option_id(a). option_id(b). option_id(c). option_id(d). option_id(e).

% Thorne assignment for each option (complete assignment to Thorne)
option_thorne(a, frost). option_thorne(a, gonzalez). option_thorne(a, heideck). option_thorne(a, mays).
option_thorne(b, frost). option_thorne(b, heideck). option_thorne(b, knutson). option_thorne(b, mays).
option_thorne(c, gonzalez). option_thorne(c, knutson). option_thorne(c, lai).
option_thorne(d, gonzalez). option_thorne(d, knutson). option_thorne(d, mays).
option_thorne(e, knutson). option_thorne(e, mays).

% For each option, define Thorne assignment
assigned_thorne(P, O) :- option_thorne(O, P).

% Remaining photographers for each option (not assigned to Thorne)
remaining(P, O) :- photographer(P), option_id(O), not assigned_thorne(P, O).

% Choice rule: assign remaining photographers to Silva or not
{ assigned_silva(P, O) } :- remaining(P, O).

% Constraint 1: At least two photographers assigned to Silva for each option
:- option_id(O), #count{P : assigned_silva(P, O)} < 2.

% Constraint 2: No photographer assigned to both ceremonies (automatically satisfied by construction)

% Constraint 3: Frost and Heideck must be together
% If Frost assigned to Thorne, Heideck must be assigned to Thorne
:- assigned_thorne(frost, O), not assigned_thorne(heideck, O).
% If Frost assigned to Silva, Heideck must be assigned to Silva
:- assigned_silva(frost, O), not assigned_silva(heideck, O).

% Constraint 4: If Lai and Mays are both assigned, they must be to different ceremonies
:- assigned_thorne(lai, O), assigned_thorne(mays, O).
:- assigned_silva(lai, O), assigned_silva(mays, O).

% Constraint 5: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
:- assigned_silva(gonzalez, O), not assigned_thorne(lai, O).

% Constraint 6: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
:- option_id(O), not assigned_thorne(knutson, O), not assigned_thorne(heideck, O).
:- option_id(O), not assigned_thorne(knutson, O), not assigned_thorne(mays, O).

% Define possible options (those that appear in some model)
option_possible(O) :- option_id(O), assigned_thorne(_, O).

% Output which options are possible
#show option_possible/1.