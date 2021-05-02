# Usage:  mridefacer [OPTIONS] <imagefile> [<imagefile> [...]]
#
#
# Options:
#
# --apply
#   If this flag is set, the defacing is applied to the input images.
#   By default, defacing mask images are created only. If --outdir is
#   not provided, the actual input images will be replaced by defaced
#   versions. In this case, the resulting images will be in FSL's
#   standard radiological orientation.
#
# -h, --help
#   Print short description, usage summary and option list.
#
# --no-colored
#   If set, mridefacer won't colorize its status and error messages.
#
# --outdir
#   If set, output files will be put into this directory. By default,
#   output files are placed in the same directory as the respective input
#   files.
#
# --verbose
#   Enable additional status messages.
#
# --verbose-help
#   Print all available help.
#
# --version
#   Print version information and exit.

# TODO: Expose all the parameters (and prob. set up argparse for that)


if __name__ == '__main__':

    import sys
    import os.path as op
    from datalad.api import Dataset
    from datalad.config import anything2bool

    dataset = Dataset(sys.argv[1])
    anonymize = anything2bool(sys.argv[2])
    files = sys.argv[3:]

    dataset.containers_run(
            ['mridefacer', '--apply'] + files,
            sidecar=anonymize,
            container_name=op.relpath(
                op.join(op.dirname(op.realpath(__file__)), "mridefacer.simg"),
                dataset.path),
            inputs=files,
            outputs=[dataset.path],
            explicit=True,
            expand="both",
            message="[HIRNI] Deface MRI data"
    )

    # TODO: re dropping:
    #       do we get a save result and run-okay or sth?
    #       -> get "files" keys from parent commit and drop them?
    #       -> or tag/branch before and delete tag/branch after drop
