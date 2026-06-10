+++
date = "2026-06-10T14:36:58-09:00"
short_text = ""
title = "A Small Key-Value Store for Large Scientific Images"
[[authors]]
    name = "Thomas Bryce Kelly"
    id = "Thomas Bryce Kelly"
    is_member = true
+++

# A Small Key-Value Store for Large Scientific Images

Modern technical computing projects often reach a point where the database is not the right place for the data.

For _Pelagia_, a plankton image analysis suite, that point arrives quickly. A single instrument run can produce large 4–30 megapixel images, intermediate masks, thumbnails, machine-learning artifacts, and derived binary products. These objects are important to the scientific record, but they are not always a good fit for direct storage inside a PostgreSQL database. PostgreSQL is excellent for metadata, relationships, provenance, query logic, project state, and analysis results. It is less attractive as a bulk object store for large, opaque binary payloads that mostly need to be written once and fetched by key.

The `kvstore` module solves that problem with a deliberately simple design: keep PostgreSQL focused on structured metadata, and store large binary blobs in a local, content-addressed key-value store backed by many small SQLite databases.

## The problem: large binary data in scientific workflows

Scientific image-analysis systems tend to accumulate binary data in layers. There is the original image, then corrected or cropped versions, segmentation masks, model inputs, model outputs, visual overlays, diagnostic snapshots, and sometimes serialized intermediate products. In a plankton imaging workflow, each object may be tens to hundreds of megabytes. The system needs to keep them findable, reproducible, and durable without turning the main relational database into a bulk storage engine.

The naive options all have tradeoffs.

Storing blobs directly in PostgreSQL simplifies references but can make backup, replication, migration, and database maintenance heavier than necessary. Storing files directly in a directory is simple, but a flat directory with millions of files eventually becomes painful, and a homegrown naming convention can become fragile. Using an object store such as S3, MinIO, or Ceph may be appropriate at larger scales, but it adds infrastructure, deployment complexity, credentials, services, and operational assumptions that may be unnecessary for a workstation, lab server, field deployment, or modest local cluster.

_Pelagia_’s `kvstore` sits in the middle. It provides object-store-like behavior using only the filesystem and SQLite.

## The core idea: content-addressed blobs

The store is content-addressed. When a payload is inserted, `kvstore` hashes the bytes and uses the hash digest as the key. By default it uses SHA-256, producing a 64-character lowercase hexadecimal key. It also supports BLAKE3 hashing if preferred.

That means the identity of an object is derived from the object itself. If two workers try to store the same image bytes, they get the same key. If a key already exists, the store checks that the existing payload matches the new payload and returns the key without creating a duplicate. If the same key were somehow associated with different bytes, the store raises an integrity error.

This is a useful property for scientific computing. It makes binary objects naturally deduplicated, reproducible, and easy to reference from a relational database. PostgreSQL can store the hash key, image metadata, sample metadata, analysis provenance, and relationships among objects, while the large bytes live outside the database.

A typical pattern is:

```python
python store = KVStore("/data/pelagia/blobstore")
store.initialize(prefix_length=4) 
image_key = store.put_store(image_bytes)  # Store image_key in PostgreSQL alongside sample ID, deployment ID, # microscope settings, segmentation status, model version, etc. 
```

Later, the application can fetch the object by key:

```python
python image_bytes = store.get_store(image_key) 
```

The key becomes the bridge between structured scientific metadata and large binary data.

## Prefix sharding: using the hash to distribute load

The most important design choice in `kvstore` is prefix sharding.

The store uses the first prefix_length hexadecimal characters of the hash key as a shard prefix. A prefix length of 2 creates 256 shard directories. A prefix length of 4 creates 65,536 shard directories. Because cryptographic hashes are approximately uniformly distributed, writes are spread randomly across those prefixes.

Each prefix directory contains one or more SQLite databases. A key beginning with a3f9... goes into the a3f9 shard when prefix_length=4. A key beginning with 7b... goes into the 7b shard when prefix_length=2.

This is a simple but powerful concurrency strategy. SQLite is reliable and lightweight, but it is not designed for many independent writers contending for the same database file. `kvstore` avoids that bottleneck by spreading writes across many SQLite files. Workers are not coordinating through one monolithic database. They are usually writing to different shard-local SQLite databases.

For example, with a prefix length of 4, there are 16⁴ = 65,536 possible prefixes. If 64 workers are continuously writing randomly distributed hash keys, the probability that at least two workers target the same shard at the same time is about 3%. That gives the system a tunable concurrency profile without introducing a network service, queue, or distributed database.

A shorter prefix length creates fewer SQLite files and less filesystem fanout. A longer prefix length creates more shard directories and lower write contention. This gives _Pelagia_ a practical migration path: adjust the prefix length when initializing a new store to match the expected workload and number of workers.

## SQLite as a blob container

Each shard is backed by SQLite, with a simple table:

```sql
CREATE TABLE blobs (     
    key TEXT PRIMARY KEY,     
    payload BLOB NOT NULL,     
    size INTEGER NOT NULL,     
    created_at TEXT NOT NULL ); 
```

This is intentionally minimal. SQLite provides atomic transactions, indexing, integrity checks, and a portable file format. The store enables `WAL` mode and uses `synchronous=NORMAL`, which is a pragmatic balance for this kind of append-heavy local object store.

The key benefits are operational rather than theoretical:

- SQLite files are easy to inspect, copy, back up, and move.  
- The store does not require a server process.  
- The payloads remain grouped into manageable database files rather than millions of loose image files.  
- The schema is explicit and versioned.  
- The implementation remains understandable to scientists and developers who already know Python and SQL.

For a technical computing project, this matters. A storage layer that is easy to reason about is more valuable than a clever one that becomes an opaque dependency.

## Rotation: keeping individual SQLite files manageable

The module also includes database rotation. Each prefix directory can contain multiple SQLite files using a filename pattern such as:

```text 
store_000001.sqlite 
store_000002.sqlite 
store_000003.sqlite 
```

Rotation is triggered when the active database exceeds either a byte threshold or a row-count threshold. By default, the limits are 4 GB per SQLite file or 1,000,000 rows. When a file reaches the configured limit, new writes for that prefix go to the next indexed SQLite file.

This protects the store from a common failure mode in long-running scientific projects: one file quietly grows until it becomes unpleasant to copy, back up, repair, move, or inspect. Rotation keeps the object store composed of bounded pieces.

Reads search the rotated files for a prefix in reverse order, starting with the most recent database. This favors recently written objects while preserving access to older data.

## File locking without heavyweight infrastructure

`kvstore` uses a small cross-platform lock based on atomic lock-file creation. There is a store-level lock used during initialization and a prefix-level lock used during writes and deletes. Lock acquisition uses `os.O_CREAT | os.O_EXCL`, which makes lock-file creation atomic on normal filesystems.

This is not trying to be a distributed lock manager. It is a practical concurrency mechanism for local disks, lab servers, and shared filesystems where many Python workers may be processing image batches. The lock includes timeout behavior, polling, and stale-lock cleanup. If a worker crashes while holding a lock, the stale lock can eventually be removed.

The important design point is that locking happens at the prefix level. A worker writing to prefix `0a91` does not block a worker writing to prefix `e442`, for example. As the prefix length increases, the probability of independent workers colliding on the same lock decreases.

## Health checks and explicit configuration

A useful storage system needs to be inspectable. The module writes a config.json and a manifest.json when initialized. These record the hash algorithm, prefix length, shard count, SQLite filename pattern, rotation policy, schema version, and creation time.

The `status()` method reports high-level store information, including:

text root path initialization state hash algorithm prefix length number of prefix directories total SQLite files total SQLite file bytes rotation settings largest SQLite file size total stored blobs total stored payload bytes largest row count 

The `check_health()` method verifies that the expected prefix directories exist, SQLite files follow the expected naming pattern, schemas are valid, and SQLite integrity checks pass.

That matters for _Pelagia_ because image analysis pipelines can run for long periods and produce data incrementally. It is not enough to store bytes; the system also needs to support maintenance, diagnostics, and confidence checks.

## Why not just store images as files?

A common alternative would be to write each image or binary object directly to the filesystem under its hash name. That approach can work, and it is conceptually simple. But SQLite adds several advantages.

First, SQLite avoids having a separate inode for every object. For workflows that may eventually produce millions of blobs, this can be more manageable than a filesystem object per payload. Second, SQLite gives the store a real schema, primary-key enforcement, row counts, byte totals, timestamps, and integrity checks. Third, rotation gives the project a predictable file layout. Instead of one giant database or an unbounded sea of files, _Pelagia_ gets a structured collection of bounded SQLite containers.

The result is still simple enough to migrate. The key is the content hash. A PostgreSQL record only needs to know the hash key and enough metadata to interpret the object. The physical storage strategy can evolve later.

## Why this fits _Pelagia_

_Pelagia_ needs to manage the boundary between image-heavy computation and metadata-heavy science. The image-analysis suite has to track samples, deployments, instruments, processing parameters, segmentation results, model versions, and quality-control state. That information belongs in PostgreSQL. But the image bytes and binary artifacts do not need to live there.

The `kvstore` module gives _Pelagia_ a local blob layer with several properties that are particularly useful for plankton image analysis:

1. It is content-addressed, so objects are reproducible and deduplicated.  
2. It is shardable, so concurrent workers can write with low collision probability.  
3. It is SQLite-backed, so it is portable, inspectable, and operationally modest.  
4. It supports rotation, so individual storage files stay within configured bounds.  
5. It has explicit configuration and health checks, so the store can be audited.  
6. It keeps migration simple because the application-level reference is just a hash key.

This architecture lets PostgreSQL remain the source of truth for scientific metadata while the kvstore handles the bulky binary layer.

## A small module with a large role

The strength of `kvstore` is not that it tries to replace object storage, PostgreSQL, or a distributed filesystem. Its strength is that it solves a constrained problem directly.

Technical computing projects often need exactly this kind of component: something more disciplined than a folder full of files, but much lighter than deploying object-storage infrastructure. The module gives _Pelagia_ a practical storage primitive that can run on a laptop, workstation, lab server, or analysis node. It gives parallel image-processing workers a way to write large artifacts without all contending for one database. It gives the project an easy reference model: the hash key identifies the object.

For _Pelagia_, that means the storage layer can support the science without becoming the science. The project can focus on plankton images, ecological signals, model outputs, and reproducible analysis, while `kvstore` quietly handles the large binary objects that make the workflow possible.