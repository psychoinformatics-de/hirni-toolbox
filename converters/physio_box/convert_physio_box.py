#!/usr/bin/env python

# convert physio data into releasable form, but do not
# apply interpolation/downsampling

import numpy as np
# from scipy import signal
# import pylab as pl


def find_triggers(tc):
    onvals = tc > tc[~np.isnan(tc)].max() * 0.8
    ramps = np.diff(onvals.astype(int))
    triggers = []
    on_state = None
    for i, r in enumerate(ramps):
        if i == 0 and onvals[i] > 0:
            # special case: start of series with trigger on
            triggers.append(i)
            on_state = True
        if r == 0:
            continue
        elif r < 0:
            if on_state is None:
                triggers.append(i)
            on_state = False
        elif r > 0:
            if not on_state:
                triggers.append(i)
            on_state = True
    return triggers


def proc_physio_run(data):
    trigger_pos = np.array(find_triggers(data[3]))
    # determine median trigger distance
    # this will allow us to distingiush 100Hz and 200Hz data
    trigger_dist = int(np.median(np.diff(trigger_pos)))

    # TODO: Move the following into some test
    #missing_triggers = expected_triggers - len(trigger_pos)
    #if missing_triggers < 0:
    #    raise RuntimeError('found more triggers than expected -> going home')

    t_peakmarker = np.zeros(data[0].shape, np.int)
    t_peakmarker[trigger_pos] = 1

    max_duration = trigger_pos[-1] + trigger_dist

    data = np.vstack((
            #trigger
            t_peakmarker,
            # respiratory
            data[0],
            # cardiac
            data[1],
            # oxygen saturation
            data[2],
        ))

    # Note: Logging disabled for now. Not yet clear where to put it.
    # if trigger_pos[0] > 0:
    #     print >>log, "Stripping %i data samples before first trigger" % trigger_pos[0]

    # cut timeseries from start to one trigger distance after the last
    data = data[:, trigger_pos[0]:max_duration]

    return data


if __name__ == '__main__':
    import sys
    import os.path as op

    # TODO: This isn't nice. Proper argparse needed.
    in_file = sys.argv[1]
    # out_dir = sys.argv[2]
    # Note: converter will be run from within BIDS ds root!
    subject = sys.argv[2]
    task = sys.argv[3]
    run = sys.argv[4]
    frequency = sys.argv[5]
    if len(sys.argv) > 6:
        session = sys.argv[6]
    else:
        session = None
    if len(sys.argv) > 7:
        recording = sys.argv[7]
    else:
        recording = "cardresp"

    # TODO: Move the following into some test
    # number of triggers that should be in each run
    # trigger_n = (451, 441, 438, 488, 462, 439, 542, 338)

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

    print('%s -> %s' % (in_file, out_file))
    data = np.loadtxt(in_file)
    d = proc_physio_run(data)

    descriptor = {"SamplingFrequency": frequency,
                  "StartTime": 0.0,
                  "Columns": ["trigger",
                              "respiratory",
                              "cardiac",
                              "oxygen saturation"]
                  }
    # TODO:       "ContentDescription": ""

    from datalad.support import json_py
    json_py.dump(descriptor, out_file_json)
    np.savetxt(out_file_tsv, d.T, delimiter='\t')





    # Note: Logging disabled for now
    #if len(sys.argv) >3:
    #    log = open(os.path.join(od,sys.argv[3]), 'w')
    #else:
    #    log = sys.stderr
