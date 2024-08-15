% depth_range(0,8)
#const depth=8.
state_id(0..depth-1).

clumsy_node(F,next(G)) :- next(F,G).
clumsy_node(F,weak_next(G)) :- weak_next(F,G).
state(0, R) :- root(R), not clumsy_node(R,_).
state(0, F) :- root(R), clumsy_node(R,F).

expandable(F) :- conjunction(F,_).
expandable(F) :- disjunction(F,_).
expandable(F) :- until(F,_,_).
expandable(F) :- release(F,_,_).

-empty(T) :- state(T, next(F)).
-empty(T) :- state(T, F), expandable(F).
empty(T) :- reached_depth(T), not -empty(T), not conflict(T).


conflict(T) :- state(T,F), state(T,G), atomic(F,L), atomic(G,-L).
conflict(T) :- state(T,false).
conflict(T) :- state(T,-true).

diff(T,T') :- T < T', state(T',_), state(T,F), not state(T',F).
diff(T,T') :- T < T', state(T,_), state(T',F), not state(T,F).
loop(T') :- T < T', not diff(T,T'), reached_depth(T), reached_depth(T').

close_branch(T) :- empty(T).
close_branch(T) :- conflict(T).
close_branch(T) :- loop(T).
open_branch(T) :- reached_depth(T), not close_branch(T).

expand(T) :- state(T,F), expandable(F).
progress(T) :- state(T,next(F)), not expand(T), not close_branch(T).
progress(T) :- state(T,weak_next(F)), not expand(T), not close_branch(T).

% Big choice rule to model which expansion rules are available in a given state
% useful for debugging
%{
%  expand_until_left(T,F): state(T,F), until(F,_,_);
%  expand_until_right(T,F): state(T,F), until(F,_,_);
%  expand_conjunction(T,F): state(T,F), conjunction(F,_);
%  expand_disjunction(T,F): state(T,F), disjunction(F,_);
%  expand_release_left(T,F): state(T,F), release(F,_,_);
%  expand_release_right(T,F): state(T,F), release(F,_,_)
%} = 1 :- expand(T), open_branch(T).

{ expand_until_left(T,F); expand_until_right(T,F) } = 1 :- state(T,F), until(F,_,_), expand(T), open_branch(T).
{ expand_release_left(T,F); expand_release_right(T,F) } = 1 :- state(T,F), release(F,_,_), expand(T), open_branch(T).
expand_conjunction(T,F) :- state(T,F), conjunction(F,_), expand(T), open_branch(T).
expand_disjunction(T,F) :- state(T,F), disjunction(F,_), expand(T), open_branch(T).

affected(T,G) :- expand_until_left(T,G).
affected(T,G) :- expand_until_right(T,G).
affected(T,G) :- expand_conjunction(T,G).
affected(T,G) :- expand_disjunction(T,G).
affected(T,G) :- expand_release_right(T,G).
affected(T,G) :- expand_release_left(T,G).

reached_depth(T) :- state(T,_), state_id(T).
:- reached_depth(T), not reached_depth(T+1), open_branch(T).

pre_state(T+1,F) :- state(T,F), not affected(T,F), expand(T), state_id(T+1).

pre_state(T+1,LHS) :- expand_until_left(T,F), until(F,LHS,RHS).
pre_state(T+1,next(F)) :- expand_until_left(T,F), until(F,LHS,RHS).
pre_state(T+1,RHS) :- expand_until_right(T,F), until(F,LHS,RHS).

pre_state(T+1, LHS) :- expand_release_left(T,F), release(F,LHS,RHS).
pre_state(T+1, RHS) :- expand_release_left(T,F), release(F,LHS,RHS).
pre_state(T+1, weak_next(F)) :- expand_release_right(T,F), release(F,LHS,RHS).
pre_state(T+1, RHS) :- expand_release_right(T,F), release(F,LHS,RHS).

pre_state(T+1,G) :- expand_conjunction(T,F), conjunction(F,G).
1 { pre_state(T+1,G): disjunction(F,G) } :- expand_disjunction(T,F).

pre_state(T+1,F) :- progress(T), state(T,next(F)).
pre_state(T+1,F) :- progress(T), state(T,weak_next(F)).

state(T+1,F) :- pre_state(T+1,F), not clumsy_node(F,_).
state(T+1,F) :- pre_state(T+1,G), clumsy_node(G,F).

result(sat) :-   close_branch(T), empty(T).
result(unsat) :- close_branch(T), conflict(T).
result(unsat) :- close_branch(T), loop(T).

:~ open_branch(T), not result(sat). [30@3]
:~ result(unsat), close_branch(T). [20@2]
:~ result(sat). [10@1]
%:- reached_depth(T), not reached_depth(T+1), open_branch(T).
%:~ result(unsat). [1@1]
%:~ result(sat).   [0@1]

#show state/2.
#show loop/1.
#show expand/1.
#show conflict/1.
#show progress/1.
#show open_branch/1.
#show close_branch/1.
#show expand_conjunction/2.
#show expand_disjunction/2.
#show expand_until_left/2.
#show expand_until_right/2.
#show expand_release_left/2.
#show expand_release_right/2.
#show empty/1.
#defined state/2.
#defined loop/1.
#defined expand/1.
#defined conflict/1.
#defined progress/1.
#defined open_branch/1.
#defined close_branch/1.
#defined result/1.
#defined empty/1.
#defined until/3.
#defined release/3.
#defined conjunction/2.
#defined disjunction/2.
#defined next/2.
#defined weak_next/2.
#defined atomic/2.
