% ==============================
% Combinatorial Auction Problem
% ==============================

% --- Domain: Bidders ---
bidder(a). bidder(b). bidder(c). bidder(d).

% --- Domain: Items ---
item(item1). item(item2). item(item3). item(item4). item(item5).

% --- Bid Data ---
% bid(BidID, Bidder, Price)
bid(1, a, 100).
bid(2, a, 50).
bid(3, b, 120).
bid(4, b, 80).
bid(5, c, 150).
bid(6, d, 40).

% --- Bundle Items for Each Bid ---
% bid_item(BidID, Item)
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

% --- Choice: Which bids win ---
{ win(BidID) } :- bid(BidID, _, _).

% --- Constraint 1: No conflicts ---
% Each item can be allocated to at most one winning bid.
% If two different bids both win and both contain the same item, that's a conflict.
:- win(B1), win(B2), B1 < B2, bid_item(B1, I), bid_item(B2, I).

% --- Derived: Item Allocation ---
% An item is allocated to a bidder if a winning bid contains that item.
allocated(Item, Bidder) :- win(BidID), bid(BidID, Bidder, _), bid_item(BidID, Item).

% --- Derived: Total Revenue ---
total_revenue(S) :- S = #sum { Price, BidID : win(BidID), bid(BidID, _, Price) }.

% --- Optimization: Maximize Revenue ---
#maximize { Price, BidID : win(BidID), bid(BidID, _, Price) }.

% --- Output ---
#show win/1.
#show allocated/2.
#show total_revenue/1.