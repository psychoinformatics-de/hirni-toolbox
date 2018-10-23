if __name__ == '__main__':

    # arguments:
    # dataset
    # rel_spec_path
    # anonymize
    # spec
    # subject
    # replacements?


    import sys
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
    run_results = list()
    with patch.dict('os.environ',
                    {'HIRNI_STUDY_SPEC': rel_spec_path,
                     'HIRNI_SPEC2BIDS_SUBJECT': subject}):

        for r in dataset.containers_run(
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
                 '-b',
                 '-a', '{dspath}',
                 '-l', '',
                 # avoid glory details provided by dcmstack,
                 # we have them in the aggregated DICOM
                 # metadata already
                 '--minmeta',
                 '--files', location
                 ],
                sidecar=anonymize,

                # TODO: This doesn't work!
                container_name="tools/heudiconv",
                inputs=[location,
                        rel_spec_path],
                outputs=[dataset.path],
                message="[HIRNI] Convert DICOM data for subject {}"
                        "".format(subject),





                # TODO: No generator; we can't yield results from a procedure





                return_type='generator',
        ):

            print(r)


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
    # remove empty *_events.tsv files created by heudiconv
    import glob
    remove_paths = glob.glob('*/*/*_events.tsv')
    if remove_paths:
        dataset.remove(remove_paths,
                       check=False,
                       message="[HIRNI] Remove empty *_event.tsv "
                               "files")
