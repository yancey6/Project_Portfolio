class SingleLinkedList:

    class _Node:
        """Lightweight, nonpublic class for storing a singly linked node."""

        def __init__(self, element, next):      # initialize node's fields
            self._element = element               # reference to user's element
            self._next = next                     # reference to next node

    def __init__(self):
        """Create an empty linkedlist."""
        self._head = None
        self._size = 0

    def __len__(self):
        """Return the number of elements in the linkedlist."""
        return self._size

    def is_empty(self):
        """Return True if the linkedlist is empty."""
        return self._size == 0

    def top(self):
        """Return (but do not remove) the element at the top of the linkedlist.

        Raise Empty exception if the linkedlist is empty.
        """
        if self.is_empty():
            raise Empty('list is empty')
        return self._head._element              # head of list

    def insert_from_head(self, e):
        """Add element e to the head of the linkedlist."""
        # Create a new link node and link it
        new_node = self._Node(e, self._head)
        self._head = new_node
        self._size += 1

    def delete_from_head(self):
        """Remove and return the element from the head of the linkedlist.

        Raise Empty exception if the linkedlist is empty.
        """
        if self.is_empty():
            raise Empty('list is empty')
        to_return = self._head._element
        self._head = self._head._next
        self._size -= 1
        return to_return

    def __str__(self):
        result = []
        curNode = self._head
        while (curNode is not None):
            result.append(str(curNode._element) + "-->")
            curNode = curNode._next
        result.append("None")
        return "".join(result)

    def __getitem__(self, k):
        """
        return the element (not the node) stored at kth indexed node.
        index range: [0, len(self) - 1]

        Example (l1):
        'hi' --> 'haha' --> 'nice' --> "good" --> None
        l1[0] ==> 'hi' is returned

        :param k: Int -- the index.
        :return: Any -- the value stored at kth indexed node.
        """
        # To do
        trial=self._head
        for i in range(k):
            trial=trial._next
        return trial._element




    def list_reverse(self):
        """
        reverses self SingleLinkedList.
        Example (l1):
        1 --> 2 --> 3 --> 4 --> None
        >>> l1.list_reverse(), then l1 becomes:
        4 --> 3 --> 2 --> 1 --> None

        :return: Nothing, modify self in place.
        """
        # To do
        target=[]
        for i in range(self._size):
            target.append(self.delete_from_head())
        for i in target:
            self.insert_from_head(i)






    def remove_all_occurance(self, value):
        """
        remove any node that contains value in self SingleLinkedList. Return nothing.
        Example:
        l1: 5 --> 4 --> 2 --> 4 --> 1 --> 9 --> 4 --> None
        >>> l1.remove_all_occurance(4)
        l1 should become: 5 --> 2 --> 1 --> 9 --> None

        :param value: Any - the value we are trying to remove from the self list.
        :return: Nothing, modify self SingleLinkedList in place
        """
        # To do
        trail=self._head
        if trail._element==value:
            self.delete_from_head()
        n=self._size
        for i in range(n-1):
            if trail._next._element==value:
                target=trail._next
                trail._next=trail._next._next
                target._next=None
                self._size-=1
            else:
                trail=trail._next

        if self._size==0:
            return


        if self._head._element==value:
            self.delete_from_head()







 
def main():
    print("----------------Testing __getitem__------------------")
    l1 = SingleLinkedList()
    l1.insert_from_head('good')
    l1.insert_from_head('nice')
    l1.insert_from_head('haha')
    l1.insert_from_head('hi')        

    print(l1)
    print("index 0 of l1:", l1[0])
    print("index 1 of l1:", l1[1])
    print("index 2 of l1:", l1[2])
    print("index 3 of l1:", l1[3])

    print("----------------Testing list_reverse------------------")
    l1 = SingleLinkedList()
    for i in range(10):
        l1.insert_from_head(i)
    print(l1)  # 9-->8-->7-->6-->5-->4-->3-->2-->1-->0-->None
    l1.list_reverse()
    print(l1, "Expected: 0-->1-->2-->3-->4-->5-->6-->7-->8-->9-->None")


    print("-----------Testing remove_all_occurance-------------")
    l1 = SingleLinkedList()
    for i in range(10):
        l1.insert_from_head(6)
    print(l1)  # 6-->6-->6-->6-->6-->6-->6-->6-->6-->6-->None
    l1.remove_all_occurance(6)
    print(l1, "Expected: None")
    print()

    l1 = SingleLinkedList()
    for i in range(10):
        l1.insert_from_head(i % 2)
    print(l1)  # 1-->0-->1-->0-->1-->0-->1-->0-->1-->0-->None
    l1.remove_all_occurance(0)
    print(l1, "Expected: 1-->1-->1-->1-->1-->None")
    print()

    

if __name__ == '__main__':
    main()




