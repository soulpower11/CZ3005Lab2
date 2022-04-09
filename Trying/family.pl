father_of(joe, paul).
father_of(joe, mary).
father_of(joe, hope).
mother_of(jane, paul).
mother_of(jane, mary).
mother_of(jane, hope).

male(paul).
male(joe).
male(ralph).
male(X) :- father_of(X,Y).

female(mary).
female(jane).
female(hope).
female(X) :- mother_of(X,Y).

son_of(X,Y) :- father_of(Y,X),male(X).
son_of(X,Y) :- mother_of(Y,X),male(X).

daughter_of(X,Y) :- father_of(Y,X),female(X).
daughter_of(X,Y) :- mother_of(Y,X),female(X).

sibling_of(X,Y) :- !,father_of(Z,X),father_of(Z,Y),X\=Y.
sibling_of(X,Y) :- !,mother_of(Z,X),mother_of(Z,Y),X\=Y.

brother_of(X,Y) :- !,father_of(Z,X),father_of(Z,Y),X\=Y,male(X).
brother_of(X,Y) :- !,mother_of(Z,X),mother_of(Z,Y),X\=Y,male(X).

sister_of(X,Y) :- !,father_of(Z,X),father_of(Z,Y),X\=Y,female(X).
sister_of(X,Y) :- !,mother_of(Z,X),mother_of(Z,Y),X\=Y,female(X).
