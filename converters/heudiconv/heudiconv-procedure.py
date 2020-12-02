if __name__ == '__main__':

    # arguments:
    # dataset
    # rel_spec_path
    # anonymize
    # spec
    # subject
    # replacements?

    import sys
    import os
    import os.path as op
    from datalad.api import Dataset
    from datalad.utils import rmtree
    from datalad.config import anything2bool

    import hirni_heuristic as heuristic

    dataset = Dataset(sys.argv[1])
    rel_spec_path = sys.argv[2]
    anonymize = anything2bool(sys.argv[3])
    subject = sys.argv[4]
    location = sys.argv[5]

    from mock import patch

    from tempfile import mkdtemp

    # relative path to heuristic to be recorded by datalad-run
    heuristic_path = op.relpath(heuristic.__file__, dataset.path)

    # relative path to not-needed-heudiconv output:
    rel_trash_path = op.relpath(mkdtemp(prefix="hirni-tmp-",
                                        dir=op.join(dataset.path,
                                                    ".git")),
                                dataset.path)

    # at least narrow down the output target:
    # TODO: Ultimately more of the output path logic needs to move here in order
    # to not have datalad-run unlock everything and do expensive modification
    # checks on unrelated subtrees.
    subject_dir = op.join(dataset.path, "sub-{}".format(subject))
    outputs = [subject_dir]

    # we expect location to be a directory (with DICOMS somewhere beneath)
    if not op.isdir(location):
        raise ValueError("%s is not a directory" % location)

    from datalad.utils import with_pathsep
    # append location with /* to specify inputs for containers-run
    # we need to get those files, but nothing from within a possible .datalad
    # for example
    inputs = [with_pathsep(location) + "*", rel_spec_path]

    run_results = list()
    with patch.dict('os.environ',
                    {'HIRNI_STUDY_SPEC': rel_spec_path,
                     'HIRNI_SPEC2BIDS_SUBJECT': subject}):

        dataset.containers_run(
                ['heudiconv',
                 # XXX absolute path will make rerun on other
                 # system impossible -- hard to avoid
                 # TODO: from toolbox? config?
                 '-f', heuristic_path,
                 # leaves identifying info in run record
                 '-s', subject,
                 '-c', 'dcm2niix',
                 # TODO decide on the fate of .heudiconv/
                 # but ATM we need to (re)move it:
                 # https://github.com/nipy/heudiconv/issues/196
                 '-o', rel_trash_path,
                 # don't create template BIDS files (ex: README, CHANGES, etc)
                 '-b', 'notop',
                 '-a', '{dspath}',
                 '-l', '',
                 # avoid glory details provided by dcmstack,
                 # we have them in the aggregated DICOM
                 # metadata already
                 '--minmeta',
                 '--files', location
                 ],
                sidecar=anonymize,
                # TODO: This doesn't work! ... Well, it does. What was the problem?
                container_name=op.relpath(op.join(op.dirname(op.realpath(__file__)), "heudiconv.simg"), dataset.path),
                explicit=True,
                expand="both",
                inputs=inputs,
                # Note: Outputs determination isn't good yet. We need a way to
                # figure what exactly heudiconv produced. This is different from
                # other toolbox-procedures due to our "injection heuristic".
                outputs=outputs,
                message="[HIRNI] Convert DICOM data for subject {}"
                        "".format(subject),

                )


    #         # if there was an issue with containers-run,
    #         # yield original result, otherwise swallow:
    #         if r['status'] not in ['ok', 'notneeded']:
    #             yield r
    #
    #         run_results.append(r)
    #
    # if not all(r['status'] in ['ok', 'notneeded']
    #            for r in run_results):
    #     yield {'action': 'heudiconv',
    #            'path': spec_path,
    #            'snippet': spec_snippet,
    #            'status': 'error',
    #            'message': "acquisition conversion failed. "
    #                       "See previous message(s)."}
    #
    # else:
    #     yield {'action': 'heudiconv',
    #            'path': spec_path,
    #            'snippet': spec_snippet,
    #            'status': 'ok',
    #            'message': "acquisition converted."}

    # remove superfluous heudiconv output
    rmtree(op.join(dataset.path, rel_trash_path))
