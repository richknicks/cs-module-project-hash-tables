class HashTableEntry:
    """
    Linked List hash table key/value pair
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        # Your code here
        self.capacity = capacity
        self.storage = [None] * capacity

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        # Your code here
        # return len(self.storage)
        return len(self.capacity)

    def get_load_factor(self):
        """
        Return the load factor for this hash table.
        
        Implement this.
        """
        # Your code here

        load = 0
        for x in self.storage:
            if x != None:
                load += 1
        load_factor = load / self.capacity
        if load_factor > 0.7:
            self.resize(int(2 * self.capacity))
        elif load_factor < 0.2:
            self.resize(int(self.capacity / 2))
        return load_factor

    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # Your code here
        hash = 14695981039346656037
        for x in key:
            hash = hash ^ ord(x)
            hash = hash * 1099411628211
        return hash

    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        # Your code here
        hash = 5381
        for c in key:
            hash = (hash * 33) + ord(c)
        return hash

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        return self.fnv1(key) % self.capacity
        # return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # Your code here
        # MVP 1 code
        # self.storage[self.hash_index(key)] = value

        h = self.hash_index(key)
        current_value = self.storage[h]
        if current_value == None:
            self.storage[h] = HashTableEntry(key, value)
        else:
            new_entry = HashTableEntry(key, value)
            new_entry.next = current_value
            self.storage[h] = new_entry
        self.get_load_factor()

    def rehash_put(self, key, value):
        h = self.hash_index(key)
        current_value = self.storage[h]
        if current_value == None:
            self.storage[h] = HashTableEntry(key, value)
        else:
            new_entry = HashTableEntry(key, value)
            new_entry.next = current_value
            self.storage[h] = new_entry

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        # Your code here
        # MVP Day 1
        # curr_idx = self.hash_index(key)
        # self.storage[curr_idx] = None
        h = self.hash_index(key)
        current_node = self.storage[h]
        while current_node.next != None:
            if current_node.key == key:
                current_node.value = None
                return
            else:
                current_node = current_node.next
        if current_node.next == None:
            if current_node.key == key:
                current_node.value = None
        self.get_load_factor()

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # Your code here
        # Day 1 MVP
        # curr_idx = self.hash_index(key)
        # return self.storage[curr_idx]
        current_node = None
        for x in range(len(self.storage)):
            current_node = self.storage[x]
            while current_node != None:
                if current_node.key == key:
                    return current_node.value
                else:
                    current_node = current_node.next

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # Your code here
        pairs = {}
        for x in range(len(self.storage)):
            current_node = self.storage[x]
            if current_node == None:
                pass
            else:
                if current_node.next == None:
                    pairs[current_node.key] = current_node.value
                while current_node.next != None:
                    pairs[current_node.key] = current_node.value
                    current_node = current_node.next
        self.capacity = new_capacity
        self.storage = [None] * (self.capacity if self.capacity > 8 else 8)

        for key in pairs:
            self.rehash_put(key, pairs[key])


if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
