% Domains
person(0..11).  % 0: Agatha, 1: Butler, 2: Charles, 3: Daisy, 4: Edward, 5: Felicity, 6: George, 7: Harriet, 8: Ian, 9: Julia, 10: Kenneth, 11: Lucy
room(0..11).    % 0: Study, 1: Hall, 2: Kitchen, 3: Library, 4: Garden, 5: Dining, 6: Cellar, 7: Lounge, 8: Conservatory, 9: Bedroom, 10: Attic, 11: Garage
time(0..6).     % 0: 19:00, 1: 19:30, 2: 20:00, 3: 20:30, 4: 21:00, 5: 21:30, 6: 22:00
weapon(0..5).   % 0: Gun, 1: Knife, 2: Rope, 3: Candlestick, 4: Wrench, 5: Poison

% Adjacency
adjacent(0,1). adjacent(1,0).  % Study <-> Hall
adjacent(0,3). adjacent(3,0).  % Study <-> Library
adjacent(1,2). adjacent(2,1).  % Hall <-> Kitchen
adjacent(1,5). adjacent(5,1).  % Hall <-> Dining
adjacent(1,6). adjacent(6,1).  % Hall <-> Cellar
adjacent(1,7). adjacent(7,1).  % Hall <-> Lounge
adjacent(1,9). adjacent(9,1).  % Hall <-> Bedroom
adjacent(2,5). adjacent(5,2).  % Kitchen <-> Dining
adjacent(2,11). adjacent(11,2). % Kitchen <-> Garage
adjacent(3,4). adjacent(4,3).  % Library <-> Garden
adjacent(3,7). adjacent(7,3).  % Library <-> Lounge
adjacent(4,8). adjacent(8,4).  % Garden <-> Conservatory
adjacent(4,11). adjacent(11,4). % Garden <-> Garage
adjacent(5,7). adjacent(7,5).  % Dining <-> Lounge
adjacent(6,11). adjacent(11,6). % Cellar <-> Garage
adjacent(7,8). adjacent(8,7).  % Lounge <-> Conservatory
adjacent(7,9). adjacent(9,7).  % Lounge <-> Bedroom
adjacent(7,10). adjacent(10,7). % Lounge <-> Attic
adjacent(9,10). adjacent(10,9). % Bedroom <-> Attic

% High-confidence locations at time 4 (murder time)
high_confidence_location(0,0,4).  % Agatha: Study
high_confidence_location(11,0,4). % Lucy: Study
high_confidence_location(1,6,4).  % Butler: Cellar
high_confidence_location(2,3,4).  % Charles: Library
high_confidence_location(3,1,4).  % Daisy: Hall
high_confidence_location(4,4,4).  % Edward: Garden
high_confidence_location(5,2,4).  % Felicity: Kitchen
high_confidence_location(6,5,4).  % George: Dining
high_confidence_location(7,7,4).  % Harriet: Lounge
high_confidence_location(8,8,4).  % Ian: Conservatory
high_confidence_location(9,9,4).  % Julia: Bedroom
high_confidence_location(10,10,4).% Kenneth: Attic

% Witness statements (18 total)
% Format: witness_statement(statement_id, person, room, time)
witness_statement(1, 2, 3, 3).  % Charles was in Library at time 3
witness_statement(2, 1, 1, 3).  % Butler was in Hall at time 3
witness_statement(3, 3, 5, 3).  % Daisy was in Dining at time 3
witness_statement(4, 4, 4, 5).  % Edward was in Garden at time 5
witness_statement(5, 5, 2, 5).  % Felicity was in Kitchen at time 5
witness_statement(6, 6, 7, 5).  % George was in Lounge at time 5
witness_statement(7, 7, 7, 3).  % Harriet was in Lounge at time 3
witness_statement(8, 8, 8, 5).  % Ian was in Conservatory at time 5
witness_statement(9, 9, 9, 5).  % Julia was in Bedroom at time 5
witness_statement(10, 10, 10, 5). % Kenneth was in Attic at time 5
witness_statement(11, 11, 1, 3). % Lucy was in Hall at time 3
witness_statement(12, 0, 0, 3).  % Agatha was in Study at time 3
witness_statement(13, 2, 3, 5).  % Charles was in Library at time 5
witness_statement(14, 1, 6, 5).  % Butler was in Cellar at time 5
witness_statement(15, 3, 1, 5).  % Daisy was in Hall at time 5
witness_statement(16, 4, 4, 3).  % Edward was in Garden at time 3
witness_statement(17, 5, 2, 3).  % Felicity was in Kitchen at time 3
witness_statement(18, 6, 5, 3).  % George was in Dining at time 3

% Forensic indicators (10 total)
% Format: forensic_indicator(indicator_id, description)
forensic_indicator(1, "no_gunshot_residue").
forensic_indicator(2, "no_shell_casings").
forensic_indicator(3, "no_blunt_force").
forensic_indicator(4, "wound_blade").
forensic_indicator(5, "no_ligature_marks").
forensic_indicator(6, "clean_edged_cut").
forensic_indicator(7, "no_heavy_blood_spatter").
forensic_indicator(8, "no_powder_burns").
forensic_indicator(9, "no_toxin_in_glass").
forensic_indicator(10, "knife_missing_from_kitchen").

% Forensic indicators consistent with knife
forensic_consistent(4).  % wound_blade
forensic_consistent(5).  % no_ligature_marks
forensic_consistent(6).  % clean_edged_cut
forensic_consistent(10). % knife_missing_from_kitchen

% Hate relations
% Agatha hates everyone except the Butler
hates(0, P) :- person(P), P != 1.

% Butler hates everyone not richer than Aunt Agatha
% Butler hates everyone whom Agatha hates
hates(1, P) :- hates(0, P).

% Charles hates no one that Agatha hates
% (This is a constraint, not a fact)

% No one hates everyone
:- person(P), { hates(P, Q) : person(Q) } = 12.

% Wealth relations (irreflexive and antisymmetric)
% We need to define richer(P1, P2) facts based on the problem.
% For now, we will leave this as a choice to be constrained later.

% Killer and weapon
% Exactly one killer
1 { killer(K) : person(K) } 1.

% Killer is not the victim (no suicides)
:- killer(0).

% Killer must be in the Study at time 4
:- killer(K), not location(K, 0, 4).

% Killer hates the victim (Agatha)
:- killer(K), not hates(K, 0).

% Killer is not richer than the victim (Agatha)
% :- killer(K), richer(K, 0).

% Charles hates no one that Agatha hates
:- hates(0, P), hates(2, P).

% Weapon used is the Knife
weapon_used(1).

% Murder occurred in the Study at time 4
% (This is enforced by the killer being in the Study at time 4)

% Each person is in exactly one room at each time
1 { location(P, R, T) : room(R) } 1 :- person(P), time(T).

% Movement is local: from time T-1 to T, a person either stays in the same room or moves to an adjacent room
:- location(P, R1, T-1), location(P, R2, T), T > 0, not adjacent(R1, R2), R1 != R2.

% High-confidence locations at time 4 must be satisfied
:- high_confidence_location(P, R, 4), not location(P, R, 4).

% Witness statements: at least 14 of 18 must be true
true_witness(S) :- witness_statement(S, P, R, T), location(P, R, T).
:- { true_witness(S) } < 14.

% Forensic indicators: at least 8 of 10 must be true, and all true ones must be consistent with knife
true_forensic(F) :- forensic_indicator(F, _), forensic_consistent(F), location(0, 0, 4). % Only consider indicators if Agatha is in Study at time 4
:- { true_forensic(F) : forensic_indicator(F, _) } < 8.

% Ensure all true forensic indicators are consistent with knife
:- true_forensic(F), not forensic_consistent(F).

% Wealth relations: irreflexive and antisymmetric
% We will define some example richer relations for testing
% In a real scenario, these would be provided or derived from additional constraints.
richer(2, 0).  % Charles is richer than Agatha
richer(3, 0).  % Daisy is richer than Agatha
richer(4, 0).  % Edward is richer than Agatha
richer(5, 0).  % Felicity is richer than Agatha
richer(6, 0).  % George is richer than Agatha
richer(7, 0).  % Harriet is richer than Agatha
richer(8, 0).  % Ian is richer than Agatha
richer(9, 0).  % Julia is richer than Agatha
richer(10, 0). % Kenneth is richer than Agatha
richer(11, 0). % Lucy is richer than Agatha

% Irreflexivity: no one is richer than themselves
:- richer(P, P).

% Antisymmetry: if P1 is richer than P2, then P2 is not richer than P1
:- richer(P1, P2), richer(P2, P1).

% Killer is not richer than the victim (Agatha)
:- killer(K), richer(K, 0).

% Butler hates everyone not richer than Aunt Agatha
hates(1, P) :- person(P), not richer(P, 0).

% Display the killer
#show killer/1.