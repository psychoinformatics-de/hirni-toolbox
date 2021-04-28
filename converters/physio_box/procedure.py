if __name__ == '__main__':

    # arguments:
    # dataset
    # anonymize
    # file to convert
    # BIDS-subject
    # BIDS-task
    # BIDS-run
    # sample frequency
    # BIDS-session (optional)
    # BIDS-recording-label (optional, default "cardresp")

    import sys
    import os.path as op
    from datalad.api import Dataset
    from datalad.config import anything2bool

    dataset = Dataset(sys.argv[1])
    converter_path = op.join(op.dirname(op.realpath(__file__)),
                             'convert_physio_box.py')
    anonymize = anything2bool(sys.argv[2])
    in_file = sys.argv[3]
    subject = sys.argv[4]
    task = sys.argv[5]
    run = sys.argv[6]
    frequency = sys.argv[7]
    if len(sys.argv) > 8:
        session = sys.argv[8]
    else:
        session = None
    if len(sys.argv) > 9:
        recording = sys.argv[9]
    else:
        recording = "cardresp"

    # sub-XX/[ses-xx]/func/<matches>[_recording-<label>]_physio.tsv.gz
    # + ******.json
    out_file = "sub-{subject}".format(subject=subject)
    if session:
        out_file += "/ses-{session}".format(session=session)
    out_file += "/func/"

    matches = "sub-{subject}".format(subject=subject)
    if session:
        matches += "_ses-{session}".format(session=session)
    # TODO: This could be a lot more complicated according to BIDS:
    matches += "_task-{task}_run-{run}".format(task=task, run=run)

    out_file += "{matches}_recording-{recording}_physio".format(
            matches=matches, recording=recording)

    out_file_json = out_file + ".json"
    out_file_tsv = out_file + ".tsv.gz"

    call = "{conv} {input} {tsv} {json} {freq}".format(
            conv=converter_path,
            input=in_file,
            tsv=out_file_tsv,
            json=out_file_json,
            freq=frequency)

    dataset.run(call,
                sidecar=anonymize,
                inputs=[in_file],
                outputs=[out_file_json, out_file_tsv],
                explicit=True,
                message="[HIRNI] Convert physio box file {}".format(out_file))
