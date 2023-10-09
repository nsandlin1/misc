% Name(s): Novi Sandlin
% Date: 2/6/2023
% Course Number and Section: CSC 330 002
% Quarter: Winter 2022-23
% Project #: 2

% isEmpty/1
% Argument is a BST. Succeeds iff the tree is empty.
isEmpty(empty).

% preOrderDisplay/1
% Argument is a BST. Visits the tree nodes in preorder
% recursively and displays its data to the terminal.
preOrderDisplay(empty).
preOrderDisplay(node(X,L,R)) :- write(X), write(' '), preOrderDisplay(L), preOrderDisplay(R).

% preOrderWrite/2
% First argument is a BST and the second argument is a file
% name. Visits the tree nodes in preorder recursively and writes
% its data to the file separated by spaces.
preOrderWrite(BST,File) :- tell(File), preOrderDisplay(BST), told.

% inOrderDisplay/1 
% Argument is a BST. Visits the tree nodes in inorder
% recursively and displays its data to the terminal.
inOrderDisplay(empty).
inOrderDisplay(node(X,L,R)) :- inOrderDisplay(L), write(X), write(' '), inOrderDisplay(R).

% inOrderWrite/2 
% First argument is a BST and the second argument is a file
% name. Visits the tree nodes in inorder recursively and writes
% its data to the file separated by spaces. 
inOrderWrite(BST,File) :- tell(File), inOrderDisplay(BST), told.

% postOrderDisplay/1 
% Argument is a BST. Visits the tree nodes in postorder
% recursively and displays its data to the terminal.
postOrderDisplay(empty).
postOrderDisplay(node(X,L,R)) :- postOrderDisplay(L), postOrderDisplay(R), write(X), write(' ').

% postOrderWrite/2 
% First argument is a BST and the second argument is a file
% name. Visits the tree nodes in postorder recursively and writes
% its data to the file separated by spaces.
postOrderWrite(BST,File) :- tell(File), postOrderDisplay(BST), told.

% getMin/2 
% First argument is a BST. The second argument is matched with
% the smallest value in the tree. If the tree is empty, the second
% argument is matched with -1 OR the predicate may fail.
getMin(empty,-1).
getMin(node(X,empty,_),X).
getMin(node(X,N,_),R) :- N\=empty, getMin(N,R1), R is min(X,R1).

% getMax/2
% First argument is a BST. The second argument is matched with
% the largest value in the tree. If the tree is empty, the second
% argument is matched with -1 OR the predicate may fail.
getMax(empty,-1).
getMax(node(X,_,empty),X).
getMax(node(X,_,N),R) :- N\=empty, getMax(N,R1), R is max(X,R1).

% insert/3
% First argument is a BST and the second argument is an integer
% x. The third argument is matched with a new tree containing data
% value x inserted correctly. If x is a value already in the tree,
% then the third argument is matched with the tree unchanged.
insert(empty,X,node(X,empty,empty)). % if tree or subtree is empty
insert(node(Oldx,L,R),Oldx,node(Oldx,L,R)). % if x already in tree return curr node as is
insert(node(X,L,R),Newx,node(X,L1,R)) :- Newx<X, insert(L,Newx,L1). % if X < current X
insert(node(X,L,R),Newx,node(X,L,R1)) :- Newx>X, insert(R,Newx,R1). % if X > current X

% delete/3
% First argument is a BST and the second argument is an integer
% x. Uses recursion to delete the tree node containing data value
% x, if it exists, and adjusts nodes so that the tree remains a
% BST, which is then matched with the third argument. If the tree
% does not contain x, the third argument is matched with the tree
% unchanged. Uses the predicate getMin.
delete(node(NX,L,R),X,node(NX,L1,R)) :- L\=empty, R\=empty, X < NX, delete(L,X,L1). % recursively track to needed node.
delete(node(NX,L,R),X,node(NX,L,R1)) :- L\=empty, R\=empty, X > NX, delete(R,X,R1).
delete(node(NX,L,empty),X,node(NX,L1,empty)) :- L\=empty, delete(L,X,L1).
delete(node(NX,empty,R),X,node(NX,empty,R1)) :- R\=empty, delete(R,X,R1).
delete(node(X,L,R),X,node(Min,L,R1)) :- L\=empty, R\=empty, getMin(R,Min), write(Min), delete(R,Min,R1).
delete(empty,_,empty). % return empty tree if tree is empty
delete(node(X,empty,empty),X,empty). % just delete node if no children
delete(node(X,empty,R),X,R) :- R \= empty. % if only one child, replace deleted node with child
delete(node(X,L,empty),X,L) :- L \= empty.

% treeRead/2
% First argument is a file name. The second argument is matched
% with a BST constructed from the integers contained in the file,
% which are separated by spaces and read recursively. Uses the
% insert predicate.
treeRead(File,BST) :- readFile(File,Contents), listToTree(Contents,empty,BST).
listToTree([H|T],CBST,BST) :- insert(CBST,H,TBST), listToTree(T,TBST,BST).
listToTree([],CBST,CBST).
% get file contents
readFile(File,R) :- see(File), getContents([],R1), doctored(R1,R), seen.
% doctor contents
doctored(L,R) :- intListGetter(L,R1), removeSpaces(R1,R2), g(R2,[],R).
% convert from list of list of string-nums to list of nums
g([H|T],C,R) :- g1num(H,'',R1), append(C,[R1],NC), g(T,NC,R).
g([],C,C).
g1num([H|T],C,R) :- atom_concat(C,H,R1), g1num(T,R1,R).
g1num([],C,R) :- atom_number(C,R).
% remove superfluous space artifact
removeSpaces([H|T],[H|R]) :- H\=[], removeSpaces(T,R).
removeSpaces([[]|T],R) :- removeSpaces(T,R).
removeSpaces([],[]).
% extract list of integers from contents
intListGetter(L,[N|R1]) :- L\=[], getNum([],L,N,RL), intListGetter(RL,R1).
intListGetter([],[]).
getNum(C,[H|T],N,RL) :- H\=' ', H\='\n', append(C,[H],C1), getNum(C1,T,N,RL).
getNum(C,[' '|T],C,T).
getNum(C,['\n'|T],C,T).
getNum(C,[],C,[]).
% get contents in list of strings
getContents(Curr,R) :- get0(C), process(C,Curr,R).
process(C,Curr,R) :- C\=(-1), char_code(Char,C), append(Curr,[Char],T), getContents(T,R).
process(-1,Curr,Curr).

% help/0
help :- write('Tree format:\n'),
	write('\tnode(X: integer, LeftNode: node, RightNode: node) or \'empty\'\n\n'),
        write('Supported functions:\n'), 
	write('\tisEmpty/1 : Argument is a BST. Succeeds iff the tree is empty.\n'),
	write('\tpreOrderDisplay/1 : Argument is a BST. Visits the tree nodes in preorder recursively and displays its data to the terminal.\n'),
	write('\tpreOrderWrite/2 : First argument is a BST and the second argument is a file name. Visits the tree nodes in preorder recursively and writes its data to the file separated by spaces.\n'),
	write('\tinOrderDisplay/1 : Argument is a BST. Visits the tree nodes in inorder recursively and displays its data to the terminal.\n'),
	write('\tinOrderWrite/2 : First argument is a BST and the second argument is a file name. Visits the tree nodes in inorder recursively and writes its data to the file separated by spaces.\n'),
	write('\tpostOrderDisplay/1 : Argument is a BST. Visits the tree nodes in postorder recursively and displays its data to the terminal.\n'),
	write('\tpostOrderWrite/2 : First argument is a BST and the second argument is a file name. Visits the tree nodes in postorder recursively and writes its data to the file separated by spaces.\n'),
	write('\tgetMin/2 : First argument is a BST. The second argument is matched with the smallest value in the tree. If the tree is empty, the second argument is matched with -1 OR the predicate may fail.\n'),
	write('\tgetMax/2 : First argument is a BST. The second argument is matched with the largest value in the tree. If the tree is empty, the second argument is matched with -1 OR the predicate may fail.\n'),
	write('\tinsert/3 : First argument is a BST and the second argument is an integer x. The third argument is matched with a new tree containing data value x inserted correctly. If x is a value already in the tree, then the third argument is matched with the tree unchanged.\n'),
	write('\tdelete/3 : First argument is a BST and the second argument is an integer x. Uses recursion to delete the tree node containing data value x, if it exists, and adjusts nodes so that the tree remains a BST, which is then matched with the third argument. If the tree does not contain x, the third argument is matched with the tree unchanged. Uses the predicate getMin.\n'),
	write('\ttreeRead/2 : First argument is a file name. The second argument is matched with a BST constructed from the integers contained in the file, which are separated by spaces and read recursively. Uses the insert predicate.\n'),
	write('\thelp/0 :  Displays to the terminal the proper tree input format and a list of all predicates/arity available.\n').
