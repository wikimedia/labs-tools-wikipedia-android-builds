#!/data/project/wikipedia-android-builds/bin/python
import os
import sh
import json
from datetime import datetime

# Environment variables required for Gradle to build app
env = {
    'ANDROID_HOME': os.path.expanduser('~/adk'),
    'ANDROID_BUILD_TOOLS': os.path.expanduser('~/adk/build-tools/20.0.0'),
    'JAVA_HOME': '/usr/lib/jvm/java-7-openjdk-amd64',
    'TERM': 'xterm-256color'
}

REPO_PATH = os.path.expanduser('~/wikipedia')

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
    run_path = os.path.expanduser('~/public_html/runs/%s' % run_slug)
    sh.mkdir('-p', run_path)

    meta['commits'] = str(sh.git('rev-list', 'HEAD..origin/master', '--oneline')).split('\n')

    sh.git('reset', '--hard', 'origin/master')

    commit_hash = str(sh.git('rev-parse', 'HEAD')).strip()

    meta['commit_hash'] = commit_hash

    # Clean out previous alpha folder
    sh.rm('-rf', '~/wikipedia/wikipedia/src/main/java/org/wikipedia/alpha')

    print 'Starting build for %s, with %s new commits' % (commit_hash, commit_count)
    sh.cd(REPO_PATH)
    gradle = sh.Command('./gradlew')
    gradle('-q', 'clean', 'assembleAlphaDebug', _env=env)

    sh.cp(sh.glob('wikipedia/build/outputs/apk/wikipedia-2.0-alpha-*.apk'), run_path)

    print 'Finished build, output at %s' % run_path

    meta['completed_on'] = datetime.now().isoformat()
    json.dump(meta, open(os.path.join(run_path, 'meta.json'), 'w'))

    latest_path = os.path.expanduser('~/public_html/runs/latest')
    sh.rm('-f', latest_path)
    sh.ln('-s', run_path, latest_path)
else:
    print 'No new commits'
