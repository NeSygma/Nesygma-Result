% --- Data ---
bid(1, "A", 100).
bid_item(1, "item1"). bid_item(1, "item2").

bid(2, "A", 50).
bid_item(2, "item3").

bid(3, "B", 120).
bid_item(3, "item2"). bid_item(3, "item3").

bid(4, "B", 80).
bid_item(4, "item4"). bid_item(4, "item5").

bid(5, "C", 150).
bid_item(5, "item1"). bid_item(5, "item3"). bid_item(5, "item5").

bid(6, "D", 40).
bid_item(6, "item4").

% --- Logic ---
% Choice rule: select a subset of bids
{ win(B) } :- bid(B, _, _).

% Constraint: No two winning bids can share an item
:- win(B1), win(B2), B1 != B2, bid_item(B1, I), bid_item(B2, I).

% Objective: Maximize total revenue
total_revenue(R) :- R = #sum { P, B : win(B), bid(B, _, P) }.
#maximize { P, B : win(B), bid(B, _, P) }.

% --- Output Mapping ---
winning_bids(B, Bidder, Price) :- win(B), bid(B, Bidder, Price).
item_allocation(Item, Bidder) :- win(B), bid(B, Bidder, _), bid_item(B, Item).

#show winning_bids/3.
#show total_revenue/1.
#show item_allocation/2.