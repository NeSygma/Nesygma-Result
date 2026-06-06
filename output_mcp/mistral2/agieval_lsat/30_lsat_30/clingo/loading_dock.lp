% Define the bays and cargo types
bay(1..6).
cargo(fuel; grain; livestock; machinery; produce; textiles).

% Each bay holds exactly one cargo type
1 { holds(Bay, Cargo) : cargo(Cargo) } 1 :- bay(Bay).

% Each cargo type is in exactly one bay
1 { holds(Bay, Cargo) : bay(Bay) } 1 :- cargo(Cargo).

% Constraints:
% 1. Grain bay > Livestock bay
:- holds(GrainBay, grain), holds(LivestockBay, livestock), GrainBay =< LivestockBay.

% 2. Livestock bay > Textiles bay
:- holds(LivestockBay, livestock), holds(TextilesBay, textiles), LivestockBay =< TextilesBay.

% 3. Produce bay > Fuel bay
:- holds(ProduceBay, produce), holds(FuelBay, fuel), ProduceBay =< FuelBay.

% 4. Textiles bay is next to Produce bay
:- holds(TextilesBay, textiles), holds(ProduceBay, produce), abs(TextilesBay - ProduceBay) != 1.

% Define the cargo in the first three bays for each option
% Option A: fuel, machinery, textiles
option(a) :- holds(1, fuel), holds(2, machinery), holds(3, textiles).

% Option B: grain, machinery, fuel
option(b) :- holds(1, grain), holds(2, machinery), holds(3, fuel).

% Option C: machinery, livestock, fuel
option(c) :- holds(1, machinery), holds(2, livestock), holds(3, fuel).

% Option D: machinery, textiles, fuel
option(d) :- holds(1, machinery), holds(2, textiles), holds(3, fuel).

% Option E: machinery, textiles, produce
option(e) :- holds(1, machinery), holds(2, textiles), holds(3, produce).

#show option/1.