class DoubleLinkedList:

    class _Node:
        """Lightweight, nonpublic class for storing a doubly linked node."""

        def __init__(self, element, prev, next):      # initialize node's fields
            self._element = element               # reference to user's element
            self._prev = prev                     # reference to prev node
            self._next = next                     # reference to next node



    def __init__(self):
        """Create an empty linkedlist."""
        self._head = self._Node(None, None, None)
        self._tail = self._Node(None, None, None)
        self._head._next = self._tail
        self._tail._prev = self._head
        self._size = 0


    def __len__(self):
        """Return the number of elements in the list."""
        return self._size

    def is_empty(self):
        """Return True if the list is empty."""
        return self._size == 0

    def _insert_between(self, e, predecessor, successor):
        """Add element e between two existing nodes and return new node."""
        newest = self._Node(e, predecessor, successor)      # linked to neighbors
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return newest

    def _delete_node(self, node):
        """Delete nonsentinel node from the list and return its element."""
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element                             # record deleted element
        node._prev = node._next = node._element = None      # deprecate node
        return element                                      # return deleted element

    def first(self):
        """Return (but do not remove) the element at the front of the list.
        Raise Empty exception if the list is empty.
        """
        if self.is_empty():
            raise Empty('list is empty')
        return self._head._next._element              # front aligned with head of list

    def last(self):
        """Return (but do not remove) the element at the end of the list.

        Raise Empty exception if the list is empty.
        """
        if self.is_empty():
            raise Empty('list is empty')
        return self._tail._prev._element


    def delete_first(self):
        """Remove and return the first element of the list.

        Raise Empty exception if the list is empty.
        """
        if self.is_empty():
            raise Empty('list is empty')
        return self._delete_node(self._head._next)

    def delete_last(self):
        """Remove and return the last element of the list.

        Raise Empty exception if the list is empty.
        """
        if self.is_empty():
            raise Empty('list is empty')
        return self._delete_node(self._tail._prev)


    def add_first(self, e):
        """Add an element to the front of list."""
        self._insert_between(e, self._head, self._head._next)


    def add_last(self, e):
        """Add an element to the back of list."""
        self._insert_between(e, self._tail._prev, self._tail)


    def __str__(self):
        result = ['head <--> ']
        curNode = self._head._next
        while (curNode._next is not None):
            result.append(str(curNode._element) + " <--> ")
            curNode = curNode._next
        result.append("tail")
        return "".join(result)


    def sameSame(self, otherlist):
        """
        Checks whether two DoubleLinkedLists lists contain the same elements in the same order
        :param otherlist: DoubleLinkedList -- the other DoubleLinkedList.

        :return: True if self list is the same as otherlist.
                 False otherwise
        """
        # To do
        trial1=self._head._next
        trial2=otherlist._head._next
        for i in range(self._size):
            if trial1._element!=trial2._element:
                return False
            else:
                trial1=trial1._next
                trial2=trial2._next
        return True

        

    def feed(self, otherlist, n):
        """
        Removes several first elements from *otherlist* and inserts them as the first
        elements of *self* list in the original order.

        Example:
        self list(l1): head <--> 5 <--> 3 <--> 2 <--> 1 <--> tail
        otherlist: head <--> 1 <--> 4 <--> 7 <--> 9 <--> tail
        >>> l1.superFeed(otherlist, 3)
        l1 should become:
            head <--> 1 <--> 4 <--> 7 <--> 5 <--> 3 <--> 2 <--> 1 <--> tail
        otherlist should become:
            head <--> 9 <--> tail

        :param otherlist: DoubleLinkedList - Remove elements from this list. (Then, add removed elements to self list.)
        :param n: Int - number of elements to remove. (You can assume n is a valid input.)
        :return: Nothing
        """

        # To do            
        target=DoubleLinkedList()
        trial=otherlist._head._next
        for i in range(n):
            target.add_last(trial._element)
            trial=trial._next
        for i in range(n):
            otherlist.delete_first()
            self.add_first(target.delete_last())


    def del_anything_occured(self, otherlist):
        """
        Remove nodes from *self* linked list, any node that contains any value appeared in *otherlist*.

        Example:
        self (l1):
        head <--> 18 <--> 16 <--> 14 <--> 12 <--> 10 <--> 18 <--> 16 <--> 14 <--> 12 <--> 10 <--> tail
        otherlist: 
        head <--> 18 <--> 16 <--> 14 <--> 12 <--> tail
        >>> l1.del_anything_occured(otherlist)
        l1 should become:
            head <--> 10 <--> 10 <--> tail
        otherlist should remain the same:
            head <--> 18 <--> 16 <--> 14 <--> 12 <--> tail

        :param otherlist: DoubleLinkedList - any value(s) appeared in this list, should get removed from self.
        :return: Nothing, modify self DoubleLinkedList in place
        """
        # To do  
        target=[]
        trail1=otherlist._head._next
        for i in range(otherlist._size):
            target.append(trail1._element)
            trail1=trail1._next

        trail2=self._head._next
        for i in range(self._size):
            if trail2._element in target:
                delete=trail2
                trail2=trail2._next
                self._delete_node(delete)
            else:
                trail2=trail2._next





def main():
    print("-------------------Testing sameSame---------------------")
    l1 = DoubleLinkedList()
    l2 = DoubleLinkedList()
    l1.add_first(1)
    l2.add_first(1)
    print(l1.sameSame(l2), "expected: True")

    for i in range(5):
        l1.add_first(i * 2)
    for j in range(5):
        l2.add_first(j * 2)
    print(l1.sameSame(l2), "expected: True")

    l1.add_first("xxx")
    l2.add_first("qqq")
    print(l1.sameSame(l2), "expected: False")


    print("-------------------Testing feed---------------------")
    l1 = DoubleLinkedList()
    l2 = DoubleLinkedList()
    for i in range(5):
        l1.add_first(i * 2)
    for j in range(5):
        l2.add_first(j * 3)
    print(l1) # 8 <--> 6 <--> 4 <--> 2 <--> 0 <--> None
    print(l2) # 12 <--> 9 <--> 6 <--> 3 <--> 0 <--> None
    l1.feed(l2, 3)
    print("Your l1:", l1, "\nExpected: head <--> 12 <--> 9 <--> 6 <--> 8 <--> 6 <--> 4 <--> 2 <--> 0 <--> tail") 
    print("Your l2:", l2, "\nExpected: head <--> 3 <--> 0 <--> tail")


    print("--------------Testing del_anything_occured----------------")
    l1 = DoubleLinkedList()
    l2 = DoubleLinkedList()
    for i in range(10):
        l1.add_first(i * 2)
    for j in range(10):
        l2.add_first(j * 3)
    print(l1)   # 18 <--> 16 <--> 14 <--> 12 <--> 10 <--> 8 <--> 6 <--> 4 <--> 2 <--> 0 <--> None
    print(l2)   # 27 <--> 24 <--> 21 <--> 18 <--> 15 <--> 12 <--> 9 <--> 6 <--> 3 <--> 0 <--> None
    l1.del_anything_occured(l2)
    print("Your l1:", l1, "\nExpected: head <--> 16 <--> 14 <--> 10 <--> 8 <--> 4 <--> 2 <--> tail")
    print("Your l2:", l2, "\nl2 should remain the same.")

 
if __name__ == '__main__':
    main()







