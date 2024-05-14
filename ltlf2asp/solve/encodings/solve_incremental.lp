#program base.

#program formula.
symbol(X) :- atomic(_,X).
node(X) :- atomic(X,_).
node(X;Y) :- next(X,Y).
node(X) :- true(X).
node(X) :- false(X).
node(X) :- last(X).
node(X;Y;Z) :- until(X,Y,Z).
node(X;Y;Z) :- release(X,Y,Z).
node(X;Y) :- negate(X,Y).
node(X;Y) :- conjunction(X,Y).
node(X;Y) :- disjunction(X,Y).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Search %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#program search(a, b).
#external search(a, b).
{ last_state(T): T=a..b-1 } = 1 :- search(a, b).
time(a..b-1) :- not search(a, b).
time(a..T) :- last_state(T), search(a, b).
{ trace(T,A): symbol(A) } :- T=a..b-1.
:- last_state(L), trace(K,_), K > L.
:- root(X), not holds(0,X), search(a,b).

#program semantics(t).
#external holds(t+1,X): node(X).
#external time(t).
#external time(t+1).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Atomic Formula %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
holds(t,X) :- atomic(X,A), trace(t,A).
holds(t,X) :- last(X), last_state(t), time(t).
holds(t,X) :- next(X,F), holds(t+1,F).
holds(t,X) :- true(X).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Temporal Formula %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
holds(t,X) :- until(X,LHS,RHS), holds(t,RHS).
holds(t,X) :- until(X,LHS,RHS), holds(t,LHS), holds(t+1,X).
holds(t, X) :- release(X, LHS, RHS), holds(t,RHS), holds(t,LHS).
holds(t, X) :- release(X, LHS, RHS), holds(t,RHS), holds(t+1, X).
holds(t, X) :- release(X, LHS, RHS), holds(t,RHS), last_state(t).

%%%%%%%%%%%%%%%%%%%%%%%%%%%% Propositional Formula %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
holds(t,X) :- negate(X,F), not holds(t,F), time(t).
holds(t,X) :- conjunction(X,_), time(t), holds(t,F): conjunction(X,F).
holds(t,X) :- disjunction(X,F), holds(t,F).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Output projection %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#show.
#show trace/2.

#defined true/1.
#defined false/1.
#defined last/1.
#defined negate/2.
#defined conjunction/2.
#defined atomic/2.
#defined disjunction/2.
#defined trace/2.
#defined next/2.
#defined until/3.
#defined release/3.
#defined last_state/1.
