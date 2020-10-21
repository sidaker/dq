-- INDEXES

CREATE INDEX "products.product_id.idx"
    ON manufacturing.products USING btree
    (product_id ASC NULLS LAST)
;

 -- btree indexes balanced or binary tree.
Most common type of index.
used for equality and range queries
High cardinality - used when large number of possible values for columns.
Time to access is based on depth of the tree. log


-- bit map
-- used for low cardinality columns. Example True, False, 0,1
-- Useful for filtering by bitwise operations such as AND , OR NOT.
-- updating can be a pain.
-- Postgres builds bitmap indexes on the fly as needed.
-- Oracle allows you to create bitmap indexes explicitly.



 -- heap


 -- hash indexes
used for equality operations
not for range of values.
smaller size than b-tree.
As fast as b-tree.
may fit in memory.



hash vs btree index?
hash -> Constant time access to index.
btree - > the depth of the tree increases at a log rate for large tables.

Does that mean hash indexes are better than binary tree indexes?


-- Bitmap
used for inclusion.
For set operations.

 -- gist
Generalized search tree.
Not a single type of index.
Frame work


 -- gin
 

 -- spgist
SP-GiST is an abbreviation for space-partitioned GiST.
SP-GiST supports partitioned search trees, which facilitate development of a
wide range of different non-balanced data structures,
such as quad-trees, k-d trees, and suffix trees (tries).

Supports partitioned search trees.
Used for non-balanced data structures

 -- Clustered vs Unclustered

 Postgres has special indexes  for geo-spatial data.
