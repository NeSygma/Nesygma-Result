% Domains
slot(1..4).
historian(farley; garcia; holden; jiang).
topic(lithographs; oil_paintings; sculptures; watercolors).

% Define earlier/2 as a fact for all Slot1 < Slot2
earier(Slot1, Slot2) :- slot(Slot1), slot(Slot2), Slot1 < Slot2.

% Assign each topic to a unique slot
1 { assigned_topic(Topic, Slot) : topic(Topic) } 1 :- slot(Slot).
:- assigned_topic(Topic1, Slot), assigned_topic(Topic2, Slot), Topic1 != Topic2.

% Assign each historian to a unique topic
1 { gives(Historian, Topic) : topic(Topic) } 1 :- historian(Historian).
:- gives(Historian, Topic1), gives(Historian, Topic2), Topic1 != Topic2.

% Each slot has exactly one topic and one historian
:- slot(Slot), not assigned_topic(_, Slot).
:- slot(Slot), not 1 { gives(_, Topic) : assigned_topic(Topic, Slot) } 1.

% Constraint 1: Oil paintings and watercolors are earlier than lithographs
:- assigned_topic(oil_paintings, Slot1),
   assigned_topic(lithographs, Slot2),
   not earlier(Slot1, Slot2).
:- assigned_topic(watercolors, Slot1),
   assigned_topic(lithographs, Slot2),
   not earlier(Slot1, Slot2).

% Constraint 2: Farley's lecture is earlier than oil paintings
:- gives(farley, Topic1),
   assigned_topic(Topic1, Slot1),
   assigned_topic(oil_paintings, Slot2),
   not earlier(Slot1, Slot2).

% Constraint 3: Holden's lecture is earlier than Garcia's and Jiang's
:- gives(holden, TopicH),
   assigned_topic(TopicH, SlotH),
   gives(garcia, TopicG),
   assigned_topic(TopicG, SlotG),
   not earlier(SlotH, SlotG).
:- gives(holden, TopicH),
   assigned_topic(TopicH, SlotH),
   gives(jiang, TopicJ),
   assigned_topic(TopicJ, SlotJ),
   not earlier(SlotH, SlotJ).

% Define the options
% (A) Farley gives the lithographs lecture
option(a) :- gives(farley, lithographs).

% (B) Garcia gives the sculptures lecture
option(b) :- gives(garcia, sculptures).

% (C) Garcia gives the watercolors lecture
option(c) :- gives(garcia, watercolors).

% (D) Holden gives the oil paintings lecture
option(d) :- gives(holden, oil_paintings).

% (E) Jiang gives the watercolors lecture
option(e) :- gives(jiang, watercolors).

% Sentinel atom to ensure at least one answer set
solution_exists.

#show option/1.
#show solution_exists/0.