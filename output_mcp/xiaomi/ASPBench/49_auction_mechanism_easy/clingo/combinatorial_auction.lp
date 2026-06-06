% ==============================
% Combinatorial Auction Problem
% ==============================

% --- Domain: Bidders ---
bidder(a).
bidder(b).
bidder(c).
bidder(d).

% --- Domain: Items ---
item(item1).
item(item2).
item(item3).
item(item4).
item(item5).

% --- Submitted Bids ---
% bid(Bidder, BidID, Price) - each bid has a unique ID
bid(a, bid1, 100).
bid(a, bid2, 50).
bid(b, bid3, 120).
bid(b, bid4, 80).
bid(c, bid5, 150).
bid(d, bid6, 40).

% --- Bundle Contents ---
% bid_item(BidID, Item) - which items are in each bid's bundle
bid_item(bid1, item1).
bid_item(bid1, item2).
bid_item(bid2, item3).
bid_item(bid3, item2).
bid_item(bid3, item3).
bid_item(bid4, item4).
bid_item(bid4, item5).
bid_item(bid5, item1).
bid_item(bid5, item3).
bid_item(bid5, item5).
bid_item(bid6, item4).

% --- Decision: Which bids win ---
% Each bid can either win or not (choice rule)
{ win(Bidder, BidID) } :- bid(Bidder, BidID, _).

% --- Constraint 1: No conflicts ---
% Each item can be allocated to at most one winning bid
% If two different bids both win and share an item, that's a conflict
:- win(_, Bid1), win(_, Bid2), Bid1 != Bid2, bid_item(Bid1, Item), bid_item(Bid2, Item).

% --- Derived: Item allocation ---
% An item is allocated to a bidder if they have a winning bid containing that item
allocated(Item, Bidder) :- win(Bidder, BidID), bid_item(BidID, Item).

% --- Derived: Total revenue ---
total_revenue(Sum) :- Sum = #sum { Price, Bidder, BidID : win(Bidder, BidID), bid(Bidder, BidID, Price) }.

% --- Objective: Maximize total revenue ---
#maximize { Price, Bidder, BidID : win(Bidder, BidID), bid(Bidder, BidID, Price) }.

% --- Show statements ---
#show win/2.
#show allocated/2.
#show total_revenue/1.