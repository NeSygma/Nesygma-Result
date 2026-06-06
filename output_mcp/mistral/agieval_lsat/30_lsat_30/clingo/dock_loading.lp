% Define the bays and cargo types
bay(1..6).

cargo(fuel; grain; livestock; machinery; produce; textiles).

% Assign each bay a unique cargo
1 { assignment(Bay, Cargo) : cargo(Cargo) } 1 :- bay(Bay).

% Ensure each cargo is assigned to exactly one bay
1 { assignment(Bay, Cargo) : bay(Bay) } 1 :- cargo(Cargo).

% Constraint 1: The bay holding grain has a higher number than the bay holding livestock
:- assignment(GrainBay, grain), assignment(LivestockBay, livestock), GrainBay <= LivestockBay.

% Constraint 2: The bay holding livestock has a higher number than the bay holding textiles
:- assignment(LivestockBay, livestock), assignment(TextilesBay, textiles), LivestockBay <= TextilesBay.

% Constraint 3: The bay holding produce has a higher number than the bay holding fuel
:- assignment(ProduceBay, produce), assignment(FuelBay, fuel), ProduceBay <= FuelBay.

% Constraint 4: The bay holding textiles is next to the bay holding produce
:- assignment(TextilesBay, textiles), assignment(ProduceBay, produce), 
   abs(TextilesBay - ProduceBay) != 1.

% Helper to get cargo at a specific bay
cargo_at(Bay, Cargo) :- assignment(Bay, Cargo).

% Define the options for the first three bays
% Option A: fuel, machinery, textiles
possible_option_a :- cargo_at(1, fuel), cargo_at(2, machinery), cargo_at(3, textiles).

% Option B: grain, machinery, fuel
possible_option_b :- cargo_at(1, grain), cargo_at(2, machinery), cargo_at(3, fuel).

% Option C: machinery, livestock, fuel
possible_option_c :- cargo_at(1, machinery), cargo_at(2, livestock), cargo_at(3, fuel).

% Option D: machinery, textiles, fuel
possible_option_d :- cargo_at(1, machinery), cargo_at(2, textiles), cargo_at(3, fuel).

% Option E: machinery, textiles, produce
possible_option_e :- cargo_at(1, machinery), cargo_at(2, textiles), cargo_at(3, produce).

% Only one option can be correct
:- possible_option_a, possible_option_b.
:- possible_option_a, possible_option_c.
:- possible_option_a, possible_option_d.
:- possible_option_a, possible_option_e.
:- possible_option_b, possible_option_c.
:- possible_option_b, possible_option_d.
:- possible_option_b, possible_option_e.
:- possible_option_c, possible_option_d.
:- possible_option_c, possible_option_e.
:- possible_option_d, possible_option_e.

% Map the correct answer to option/1
option(a) :- possible_option_a.
option(b) :- possible_option_b.
option(c) :- possible_option_c.
option(d) :- possible_option_d.
option(e) :- possible_option_e.

#show option/1.