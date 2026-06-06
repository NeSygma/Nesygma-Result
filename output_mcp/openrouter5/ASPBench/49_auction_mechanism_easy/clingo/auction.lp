%% Combinatorial Auction - Maximize Revenue

%% Domain definitions
bidder(a; b; c; d).
item(1..5).

%% Bids: bid(ID, Bidder, Price)
bid(1, a, 100).  % {item1, item2}
bid(2, a, 50).   % {item3}
bid(3, b, 120).  % {item2, item3}
bid(4, b, 80).   % {item4, item5}
bid(5, c, 150).  % {item1, item3, item5}
bid(6, d, 40).   % {item4}

%% Bundle contents: bundle(BidID, Item)
bundle(1, 1). bundle(1, 2).
bundle(2, 3).
bundle(3, 2). bundle(3, 3).
bundle(4, 4). bundle(4, 5).
bundle(5, 1). bundle(5, 3). bundle(5, 5).
bundle(6, 4).

%% Choice: which bids to accept
{ accepted(BidID) } :- bid(BidID, _, _).

%% Constraint: each item allocated to at most one bidder
%% An item is allocated if it belongs to an accepted bid
allocated_to(Item, BidID) :- accepted(BidID), bundle(BidID, Item).

%% No two accepted bids may share an item
:- accepted(B1), accepted(B2), B1 != B2, bundle(B1, I), bundle(B2, I).

%% Compute total revenue
total_revenue(S) :- S = #sum { P, ID : accepted(ID), bid(ID, _, P) }.

%% Maximize revenue
#maximize { P, ID : accepted(ID), bid(ID, _, P) }.

%% Output
#show accepted/1.
#show total_revenue/1.
#show winning_bid/3.
winning_bid(Bidder, Items, Price) :- accepted(ID), bid(ID, Bidder, Price), Items = #count { I : bundle(ID, I) }.