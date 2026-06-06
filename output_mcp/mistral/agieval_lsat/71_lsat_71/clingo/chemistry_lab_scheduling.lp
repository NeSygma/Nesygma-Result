% Days and times
day(wednesday; thursday; friday).
time(morning; afternoon).

% Day ordering for temporal constraints
day_order(wednesday, 1).
day_order(thursday, 2).
day_order(friday, 3).

% Assistants
assistant(julio; kevin; lan; nessa; olivia; rebecca).

% Each session must have exactly one assistant
1 { assigned(Day, Time, Assistant) : assistant(Assistant) } 1 :- day(Day), time(Time).

% Each assistant must be assigned to exactly one session
1 { assigned(Day, Time, Assistant) : day(Day), time(Time) } 1 :- assistant(Assistant).

% Constraint 1: Kevin and Rebecca must lead sessions on the same day
:- assigned(Day, _, kevin), not assigned(Day, _, rebecca).
:- assigned(Day, _, rebecca), not assigned(Day, _, kevin).

% Constraint 2: Lan and Olivia cannot lead sessions on the same day
:- assigned(Day, _, lan), assigned(Day, _, olivia).

% Constraint 3: Nessa must lead an afternoon session
:- assigned(Day, morning, nessa).

% Constraint 4: Julio's session must be on an earlier day than Olivia's
:- assigned(Day1, _, julio), assigned(Day2, _, olivia),
   day_order(Day1, O1), day_order(Day2, O2), O2 <= O1.

% Define the options as possible assignments
% Option A: Wednesday: Rebecca, Kevin; Thursday: Julio, Lan; Friday: Nessa, Olivia
option_a :- assigned(wednesday, morning, rebecca),
             assigned(wednesday, afternoon, kevin),
             assigned(thursday, morning, julio),
             assigned(thursday, afternoon, lan),
             assigned(friday, morning, nessa),
             assigned(friday, afternoon, olivia).

% Option B: Wednesday: Olivia, Nessa; Thursday: Julio, Lan; Friday: Kevin, Rebecca
option_b :- assigned(wednesday, morning, olivia),
             assigned(wednesday, afternoon, nessa),
             assigned(thursday, morning, julio),
             assigned(thursday, afternoon, lan),
             assigned(friday, morning, kevin),
             assigned(friday, afternoon, rebecca).

% Option C: Wednesday: Lan, Kevin; Thursday: Rebecca, Julio; Friday: Olivia, Nessa
option_c :- assigned(wednesday, morning, lan),
             assigned(wednesday, afternoon, kevin),
             assigned(thursday, morning, rebecca),
             assigned(thursday, afternoon, julio),
             assigned(friday, morning, olivia),
             assigned(friday, afternoon, nessa).

% Option D: Wednesday: Kevin, Rebecca; Thursday: Julio, Nessa; Friday: Olivia, Lan
option_d :- assigned(wednesday, morning, kevin),
             assigned(wednesday, afternoon, rebecca),
             assigned(thursday, morning, julio),
             assigned(thursday, afternoon, nessa),
             assigned(friday, morning, olivia),
             assigned(friday, afternoon, lan).

% Option E: Wednesday: Julio, Lan; Thursday: Olivia, Nessa; Friday: Rebecca, Kevin
option_e :- assigned(wednesday, morning, julio),
             assigned(wednesday, afternoon, lan),
             assigned(thursday, morning, olivia),
             assigned(thursday, afternoon, nessa),
             assigned(friday, morning, rebecca),
             assigned(friday, afternoon, kevin).

% Map to option/1
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.