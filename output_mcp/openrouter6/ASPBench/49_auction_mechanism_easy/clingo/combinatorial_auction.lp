% Combinatorial Auction Problem

% Domains
bidder(a; b; c; d).
item(item1; item2; item3; item4; item5).

% Bids: bid(BidID, Bidder, Price)
bid(1, a, 100).
bid(2, a, 50).
bid(3, b, 120).
bid(4, b, 80).
bid(5, c, 150).
bid(6, d, 40).

% Items in each bid
bid_item(1, item1).
bid_item(1, item2).

bid_item(2, item3).

bid_item(3, item2).
bid_item(3, item3).

bid_item(4, item4).
bid_item(4, item5).

bid_item(5, item1).
bid_item(5, item3).
bid_item(5, item5).

bid_item(6, item4).

% Choice: which bids win
{ winning(BidID) } :- bid(BidID, _, _).

% Constraint: each item can be allocated to at most one winning bid
:- bid_item(BidID1, Item), bid_item(BidID2, Item), winning(BidID1), winning(BidID2), BidID1 != BidID2.

% Derive item allocation from winning bids
item_allocation(Item, Bidder) :- bid_item(BidID, Item), winning(BidID), bid(BidID, Bidder, _).

% Compute total revenue
total_revenue(Revenue) :- Revenue = #sum { Price, BidID : winning(BidID), bid(BidID, _, Price) }.

% Optimization: maximize total revenue
#maximize { Price, BidID : winning(BidID), bid(BidID, _, Price) }.

% Show winning bids with details (without items list)
winning_bid(BidID, Bidder, Price) :- winning(BidID), bid(BidID, Bidder, Price).

% Show winning bid items
winning_bid_item(BidID, Item) :- winning(BidID), bid_item(BidID, Item).

% Show allocation per item
#show item_allocation/2.
% Show winning bids
#show winning_bid/3.
% Show winning bid items
#show winning_bid_item/2.
% Show total revenue
#show total_revenue/1.