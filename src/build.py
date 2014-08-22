#!/data/project/wikipedia-android-builds/bin/python
import os
import sh
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
    # Create the output directory
    run_slug = 'master-%s' % datetime.now().isoformat()
    run_path = os.path.expanduser('~/public_html/runs/%s' % run_slug)
    sh.mkdir('-p', run_path)

    sh.git('reset', '--hard', 'origin/master')

    # Run in side the app folder, since we can't run
    # instrumentation tests
    sh.cd(os.path.join(REPO_PATH, 'wikipedia'))
    mvn = sh.Command(os.path.expanduser('~/mvn/bin/mvn'))
    mvn('clean', 'install', _env=env)

    sh.cp('target/wikipedia.apk', run_path)
else:
    print 'No new commits'
