% Positive file: original claim as conjecture
% Premise 1: No digital media are analog.
fof(premise1, axiom, ! [X] : (digital_media(X) => ~analog_media(X))).
% Premise 2: Every printed text is analog media.
fof(premise2, axiom, ! [X] : (printed_text(X) => analog_media(X))).
% Premise 3: All streaming services are digital media.
fof(premise3, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
% Premise 4: If an object is a hardcover book, then it is printed text.
fof(premise4, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
% Premise 5: If 1984 is a streaming service, then 1984 is a hardcover book.
fof(premise5, axiom, (streaming_service(x1984) => hardcover_book(x1984))).
% Conclusion: 1984 is not a streaming service.
fof(goal, conjecture, ~streaming_service(x1984)).