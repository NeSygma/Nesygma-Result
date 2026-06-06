% Combinatorial Auction - Maximize Revenue

% Facts
item(1..5).           % item1, item2, item3, item4, item5
bidder(a; b; c; d).   % Bidders A, B, C, D

% Bids: bid(ID, Bidder, Price)
bid(1, a, 100).   % A: {item1, item2}
bid(2, a, 50).    % A: {item3}
bid(3, b, 120).   % B: {item2, item3}
bid(4, b, 80).    % B: {item4, item5}
bid(5, c, 150).   % C: {item1, item3, item5}
bid(6, d, 40).    % D: {item4}

% Items in each bid: bid_item(ID, Item)
bid_item(1, 1). bid_item(1, 2).
bid_item(2, 3).
bid_item(3, 2). bid_item(3, 3).
bid_item(4, 4). bid_item(4, 5).
bid_item(5, 1). bid_item(5, 3). bid_item(5, 5).
bid_item(6, 4).

% Choice: each bid can either win or not
{ win(ID) } :- bid(ID, _, _).

% Constraint: each item can be in at most one winning bid
:- item(I), #count { ID : win(ID), bid_item(ID, I) } > 1.

% Maximize total revenue
#maximize { P, ID : win(ID), bid(ID, _, P) }.

% Derived output predicates
winning_bid(ID, Bidder, Price) :- win(ID), bid(ID, Bidder, Price).

total_revenue(R) :- R = #sum { P, ID : win(ID), bid(ID, _, P) }.

assigned_item(I, Bidder) :- win(ID), bid(ID, Bidder, _), bid_item(ID, I).

% Show results
#show winning_bid/3.
#show total_revenue/1.
#show assigned_item/2.