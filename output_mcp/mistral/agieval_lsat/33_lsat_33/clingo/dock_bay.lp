% Bays and cargo types
bay(1..6).
cargo(fuel; grain; livestock; machinery; produce; textiles).

% Assign each bay to a unique cargo
1 { assigned(Bay, Cargo) : cargo(Cargo) } 1 :- bay(Bay).

% Ensure each cargo is assigned to exactly one bay
1 { assigned(Bay, Cargo) : bay(Bay) } 1 :- cargo(Cargo).

% Constraints from the problem
% 1. grain > livestock (grain bay has higher number than livestock bay)
:- assigned(GrainBay, grain), assigned(LivestockBay, livestock), GrainBay <= LivestockBay.

% 2. livestock > textiles (livestock bay has higher number than textiles bay)
:- assigned(LivestockBay, livestock), assigned(TextilesBay, textiles), LivestockBay <= TextilesBay.

% 3. produce > fuel (produce bay has higher number than fuel bay)
:- assigned(ProduceBay, produce), assigned(FuelBay, fuel), ProduceBay <= FuelBay.

% 4. textiles is next to produce (textiles bay is adjacent to produce bay)
:- assigned(TextilesBay, textiles), assigned(ProduceBay, produce), abs(TextilesBay - ProduceBay) != 1.

% Map the correct answer to option/1
option(a) :- assigned(1, livestock).
option(b) :- assigned(2, livestock).
option(c) :- assigned(3, livestock).
option(d) :- assigned(5, livestock).
option(e) :- assigned(6, livestock).

#show option/1.