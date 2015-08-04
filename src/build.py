#!/usr/bin/python
from __future__ import print_function
import os
import sh
import json
import sys
from datetime import datetime

# Environment variables required for Gradle to build app
env = {
    'HOME': '/home/android-build',
    'ANDROID_HOME': os.path.expanduser('/srv/adk'),
#    'ANDROID_BUILD_TOOLS': os.path.expanduser('/srv/adk/build-tools/20.0.0'),
    'JAVA_HOME': '/usr/lib/jvm/java-7-openjdk-amd64',
    'TERM': 'xterm-256color'
}

REPO_PATH = '/srv/wikipedia'

start = '== %s ==' % datetime.now().isoformat()
print(start, file=sys.stdout)
print(start, file=sys.stderr)

sh.cd(REPO_PATH)
sh.git('fetch')

# Only run script if we have new commits
commit_count = int(sh.git('rev-list', 'HEAD..origin/master', '--count'))

if commit_count != 0:
    meta = {
        'commit_count': commit_count
    }

    # Create the output directory
    run_slug = 'master-%s' % datetime.now().isoformat()
    run_path = '/srv/builds/public_html/runs/%s' % run_slug
    sh.mkdir('-p', run_path)

    meta['commits'] = str(sh.git('rev-list', 'HEAD..origin/master', '--oneline')).split('\n')

    sh.git('reset', '--hard', 'origin/master')

    commit_hash = str(sh.git('rev-parse', 'HEAD')).strip()

    meta['commit_hash'] = commit_hash

    print('Starting build for %s, with %s new commits' % (commit_hash, commit_count), file=sys.stdout)

    sh.cd(REPO_PATH)
    gradle = sh.Command('./gradlew')
    gradle('-q', 'clean', 'assembleAlphaDebug', _env=env)

    sh.cp(sh.glob('/srv/wikipedia/app/build/outputs/apk/app-alpha-debug.apk'),
          os.path.join(run_path, 'wikipedia.apk'))

    print('Finished build, output at %s' % run_path, file=sys.stdout)

    meta['completed_on'] = datetime.now().isoformat()
    json.dump(meta, open(os.path.join(run_path, 'meta.json'), 'w'))

    latest_path = '/srv/builds/public_html/runs/latest'
    sh.rm('-f', latest_path)
    sh.ln('-s', run_path, latest_path)
else:
    print('No new commits', file=sys.stdout)
