import subprocess
import shlex

def run(cmd, cwd=None, wait=True):
    proc = subprocess.Popen(shlex.split(cmd), cwd=cwd)
    if wait:
        proc.wait()
        return proc.returncode
    return proc
