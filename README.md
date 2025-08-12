# AVL-Tree
A Python implementation of an AVL Tree — a self-balancing binary search tree.

Supports efficient dictionary-like operations while maintaining balance for guaranteed logarithmic performance.

## Implementation Details:
Language: Python

Structure: Node-based tree with parent, left, and right references.

Tracks height and size at each node to support balancing, rank, and selection operations.

Balancing is maintained via rotations (left and right) after insertions and deletions.

### Allows the following:
Insert elements – O(log n), Delete elements – O(log n), Search by key – O(log n),

Select i-th smallest – O(log n), Find rank of a node – O(log n),

Convert to sorted array – O(n), Find max value in a key range – O(n).

### Takeaways:
Gained experience with:

- Implementing self-balancing BSTs from scratch.

- Rotation-based rebalancing and maintaining height/size metadata.

- Supporting advanced queries like rank, select, and range maximums.
