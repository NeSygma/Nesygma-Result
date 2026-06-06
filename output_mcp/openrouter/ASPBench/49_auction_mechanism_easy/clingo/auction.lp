% Bids data
bid(b1, "A", 100). % {item1, item2}
bid(b2, "A", 50).  % {item3}
bid(b3, "B", 120). % {item2, item3}
bid(b4, "B", 80).  % {item4, item5}
bid(b5, "C", 150). % {item1, item3, item5}
bid(b6, "D", 40).  % {item4}

bid_item(b1, item1). bid_item(b1, item2).
bid_item(b2, item3).
bid_item(b3, item2). bid_item(b3, item3).
bid_item(b4, item4). bid_item(b4, item5).
bid_item(b5, item1). bid_item(b5, item3). bid_item(b5, item5).
bid_item(b6, item4).

% Define items domain
item(item1). item(item2). item(item3). item(item4). item(item5).

% Choice of winning bids
{selected(B)} :- bid(B,_,_).

% Conflict constraint: each item at most one selected bid containing it
:- item(I), #count { B : selected(B), bid_item(B,I) } > 1.

% Compute total revenue
total_rev(R) :- R = #sum { P,B : selected(B), bid(B,_,P) }.

% Allocation mapping
allocation(I, Bidder) :- selected(B), bid_item(B,I), bid(B,Bidder,_).

#show selected/1.
#show total_rev/1.
#show allocation/2.