% Combinatorial Auction Problem

% Domain declarations
bidder(a). bidder(b). bidder(c). bidder(d).
item(item1). item(item2). item(item3). item(item4). item(item5).

% Bids with IDs
% Bid 1: A, {item1, item2}, $100
bid(1, a, 100).
bid_bundle(1, item1).
bid_bundle(1, item2).

% Bid 2: A, {item3}, $50
bid(2, a, 50).
bid_bundle(2, item3).

% Bid 3: B, {item2, item3}, $120
bid(3, b, 120).
bid_bundle(3, item2).
bid_bundle(3, item3).

% Bid 4: B, {item4, item5}, $80
bid(4, b, 80).
bid_bundle(4, item4).
bid_bundle(4, item5).

% Bid 5: C, {item1, item3, item5}, $150
bid(5, c, 150).
bid_bundle(5, item1).
bid_bundle(5, item3).
bid_bundle(5, item5).

% Bid 6: D, {item4}, $40
bid(6, d, 40).
bid_bundle(6, item4).

% Choice rule: Select which bids win
{winning_bid(Bid)} :- bid(Bid, _, _).

% Constraint: Each item can be allocated to at most one bidder
% If a bid wins, all items in its bundle are allocated to its bidder
item_allocated(Item, Bidder) :- winning_bid(Bid), bid(Bid, Bidder, _), bid_bundle(Bid, Item).

% Constraint: No item can be allocated to more than one bidder
:- item_allocated(Item, Bidder1), item_allocated(Item, Bidder2), Bidder1 != Bidder2.

% Constraint: If a bid wins, all items in its bundle must be allocated to its bidder
% This is already enforced by the item_allocated rule above

% Calculate total revenue
total_revenue(Revenue) :- Revenue = #sum{Price, Bid : winning_bid(Bid), bid(Bid, _, Price)}.

% Show winning bids with details
selected_bid(Bid, Bidder, Price) :- winning_bid(Bid), bid(Bid, Bidder, Price).

% Show allocation
item_allocation(Item, Bidder) :- item_allocated(Item, Bidder).

% Show total revenue
#show total_revenue/1.
#show selected_bid/3.
#show item_allocation/2.
#show winning_bid/1.