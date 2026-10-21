# Import torch up front. Native libraries loaded by this package (in particular
# diplib's JVM, pulled in via utils/file_io) can segfault when torch is imported
# for the first time *after* images have already been read. Importing torch at
# package-import time makes the native library load order deterministic.
import torch  # noqa: F401
