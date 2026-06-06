% Domain
bidder(a; b; c; d).
item(item1; item2; item3; item4; item5).

% Bids: bid(Bidder, BidID, Price, Item)
% Each bid is represented as multiple facts for its items
bid(a, 1, 100, item1). bid(a, 1, 100, item2).
bid(a, 2, 50, item3).
bid(b, 3, 120, item2). bid(b, 3, 120, item3).
bid(b, 4, 80, item4). bid(b, 4, 80, item5).
bid(c, 5, 150, item1). bid(c, 5, 150, item3). bid(c, 5, 150, item5).
bid(d, 6, 40, item4).

% Choice rule: select winning bids
{ winning_bid(BidID) : bid(_, BidID, _, _) }.

% For each winning bid, record the bidder and price
winning_bid_info(Bidder, BidID, Price) :-
    winning_bid(BidID),
    bid(Bidder, BidID, Price, _).

% Allocate items based on winning bids
allocated_to(Item, Bidder) :-
    winning_bid_info(Bidder, _, _),
    bid(Bidder, _, _, Item).

% Constraint: No item can be allocated to more than one bidder
:- allocated_to(Item, Bidder1),
   allocated_to(Item, Bidder2),
   Bidder1 != Bidder2.

% Calculate total revenue
revenue(Price) :- winning_bid_info(_, _, Price).
total_revenue(Total) :- Total = #sum { Price : revenue(Price) }.

% Objective: Maximize total revenue
#maximize { Total : total_revenue(Total) }.

% Show the results
#show winning_bid_info/3.
#show allocated_to/2.
#show total_revenue/1.