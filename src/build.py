#!/data/project/wikipedia-android-builds/bin/python
import os
import sh
import json
from datetime import datetime

# Environment variables required for mvn to build app
env = {
    'M2_HOME': os.path.expanduser('~/mvn'),
    'M2': os.path.expanduser('~/mvn'),
    'ANDROID_HOME': os.path.expanduser('~/adk'),
    'ANDROID_BUILD_TOOLS': os.path.expanduser('~/adk/build-tools/20.0.0')
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

    # Change the package name to .alpha
    prepare_release = sh.Command(os.path.expanduser('~/wikipedia/scripts/prepare-release.py'))
    prepare_release('--alpha')

    print 'Starting build for %s, with %s new commits' % (commit_hash, commit_count)
    # Run in side the app folder, since we can't run
    # instrumentation tests
    sh.cd(os.path.join(REPO_PATH, 'wikipedia'))
    mvn = sh.Command(os.path.expanduser('~/mvn/bin/mvn'))
    mvn('clean', 'install', _env=env)

    print 'Finished build, output at %s' % run_path

    sh.cp('target/wikipedia.apk', run_path)

    meta['completed_on'] = datetime.now().isoformat()
    json.dump(meta, open(os.path.join(run_path, 'meta.json'), 'w'))

    latest_path = os.path.expanduser('~/public_html/runs/latest')
    sh.rm('-f', latest_path)
    sh.ln('-s', run_path, latest_path)
else:
    print 'No new commits'
