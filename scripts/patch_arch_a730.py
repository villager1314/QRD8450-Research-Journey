#!/usr/bin/env python3
"""Verified Arch A730 table patch. Default: dry run."""
import argparse
import hashlib
import os
from pathlib import Path
import shutil
import tempfile

ORIGINAL = 'acae732269aabb9e08da23f6f3b19b67e74c3092065950ba3988b2bfec03b060'
PATCHED = 'dbef58a4aa96543ff8d2c10b453ac81e543fcecf8aee215ff4b19194463563cd'
def sha(data):
    return hashlib.sha256(data).hexdigest()

def patch(data):
    if sha(data) != ORIGINAL:
        raise ValueError('Original hash mismatch')
    out = bytearray(data)
    for offset, expected in ((0x1579bb8, 0x07030001), (0x1579bd8, 0xffff07030001)):
        if int.from_bytes(out[offset:offset+8], 'little') != expected:
            raise ValueError('GPU table record mismatch')
        out[offset] = 0
    if sha(out) != PATCHED:
        raise ValueError('Output hash mismatch')
    return out

def replace(path, data):
    st = path.stat()
    fd, tmp = tempfile.mkstemp(prefix=path.name+'.a730-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        shutil.copystat(path, tmp)
        if os.geteuid() == 0:
            os.chown(tmp, st.st_uid, st.st_gid)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('file', nargs='?', default='/usr/lib/libgallium-26.3.0-arch1.1.so')
    group = ap.add_mutually_exclusive_group()
    group.add_argument('--apply', action='store_true')
    group.add_argument('--restore', action='store_true')
    args = ap.parse_args()
    path = Path(args.file)
    if path.is_symlink() or not path.is_file():
        raise ValueError('Expected regular non-symlink file')
    data = path.read_bytes()
    current = sha(data)
    backup = path.with_name(path.name+'.before-a730-patch')
    print('SHA-256:', current)
    if args.restore:
        if current != PATCHED:
            raise ValueError('Current file is not verified patched version')
        if backup.is_symlink() or not backup.is_file():
            raise ValueError('Expected regular backup file')
        original = backup.read_bytes()
        if sha(original) != ORIGINAL:
            raise ValueError('Backup hash mismatch')
        replace(path, original)
        print('Restored original; backup retained')
        return
    if current == PATCHED:
        print('Already patched; no changes')
        return
    out = patch(data)
    if not args.apply:
        print('Verified two-byte patch applicable; dry run, no changes')
        return
    if backup.exists() or backup.is_symlink():
        if backup.is_symlink() or not backup.is_file() or sha(backup.read_bytes()) != ORIGINAL:
            raise ValueError('Invalid existing backup; refusing to overwrite')
    else:
        with backup.open('xb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        shutil.copystat(path, backup)
    replace(path, out)
    print('Patch applied; backup:', backup)

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(str(error))
