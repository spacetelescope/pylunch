#!/usr/bin/env python
"""
A script to automate copying over the slides from the sessions

Note that this will overwrite the git index, so make sure you commit anything
before running this.
"""


def generated_html_slides(basedir, dirs):
    import os
    import sys
    from glob import glob

    generated_html = []
    for dirnm in dirs:
        os.chdir(os.path.join(basedir, dirnm))
        for nbnm in glob(os.path.join('*.ipynb')):
            retcode = os.system('jupyter nbconvert --to slides "{}" '
                                '--reveal-prefix ../reveal.js'.format(nbnm))
            if retcode != 0:
                print('Bailing out because slide conversion failed.')
                sys.exit(retcode)

            generated_html.append(os.path.join(dirnm, nbnm[:-6] + '.slides.html'))

    return generated_html


def make_index(toindex, fntowrite='index.html'):
    lines = ['<!DOCTYPE html>']

    lines.append('<html>')
    lines.append('<body>')

    lines.append('<ul>')
    for fn in sorted(toindex):
        lines.append('<li><a href="{0}">{0}</a></li>'.format(fn))
    lines.append('</ul>')

    lines.append('</body>')
    lines.append('</html>')

    with open(fntowrite, 'w') as f:
        for l in lines:
            f.write(l)
            f.write('\n')


def update_pages_branch(remote_to_push_to, pages_branch, dirs, push_if_no_update):
    import os

    import git  # GitPython

    repo = git.Repo()
    for branch in repo.branches:
        if branch.name == pages_branch:
            break
    else:
        raise ValueError('Found no branch named ' + str(pages_branch))

    orig_ref = repo.head.reference

    repo.head.reference = branch
    repo.head.reset(index=True, working_tree=False)

    toadd = []
    for dirnm in dirs:
        for dirpath, dirnames, filenames in os.walk(dirnm):
            for fnm in filenames:
                if not fnm.endswith('.ipynb'):
                    toadd.append(os.path.join(dirpath, fnm))

    if os.path.isfile('index.html'):
        toadd.append('index.html')

    repo.index.add(toadd)
    anything_added = repo.git.diff('--cached', '--abbrev=40', '--raw') != ''
    if anything_added or push_if_no_update:
        repo.index.commit('Automatic commit from update_pages.py')

        if remote_to_push_to:
            for remote in repo.remotes:
                if remote.name == remote_to_push_to:
                    break
            else:
                raise ValueError('Found no remote named ' + str(remote_to_push_to))

            pushres = remote.push(pages_branch)
            push_errored = len(pushres) == 0
            if not push_errored:
                push_errored = any([bool(r.flags&r.ERROR) for r in pushres])
            if push_errored:
                print('Pushing {} to {} failed - try manually for more '
                      'info'.format(pages_branch, remote_to_push_to))
            else:
                print('Pushed {} to {} without any errors'.format(pages_branch,
                                                                  remote_to_push_to))
        else:
            print('Not pushing {} to any remote'.format(pages_branch))
    else:
        print("Nothing to be added, so not committing and not pushing")

    repo.head.reference = orig_ref
    repo.head.reset(index=True, working_tree=False)


def main(remote, pages_branch, pattern, push_if_no_update):
    import re
    import os

    basedir = os.path.abspath('')

    rex = re.compile(pattern)
    dirs_to_copy = [name for name in os.listdir() if rex.match(name) and
                                                     os.path.isdir(name)]
    generated_html = generated_html_slides(basedir, dirs_to_copy)

    os.chdir(basedir)

    make_index(generated_html)
    update_pages_branch(remote, pages_branch, dirs_to_copy, push_if_no_update)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--remote', default=None, help='The name of '
                        'the remote to push to.  Defaults to not pushing')
    parser.add_argument('-b', '--pages-branch', default='gh-pages', help='The '
                        'name of the github pages branch')
    parser.add_argument('-p', '--pattern', default=r'^(?!scripts)',
                        help='A regular expression to identify the directories'
                             ' to be copied')
    parser.add_argument('-n', '--push-if-no-update', action='store_true',
                        help='The name set to push to the remote even if no '
                        'changes were detected.')
    ns = parser.parse_args()

    main(ns.remote, ns.pages_branch, ns.pattern, ns.push_if_no_update)
