# Shared paths: the repository root, and the working folder for scans, page files, corpora and judge batches
# (NLE_WORK, default <repository>/work, which git ignores).
import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK = os.environ.get('NLE_WORK', os.path.join(ROOT, 'work'))
