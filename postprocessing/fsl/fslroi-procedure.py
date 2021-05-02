if __name__ == '__main__':

    import sys
    import os.path as op
    from datalad.api import Dataset
    dataset = Dataset(sys.argv[1])

    params = []
    delimiter = None
    for i, p in enumerate(sys.argv[2:]):
        if p == '--':
            delimiter = i
            break
        else:
            params.append(p)
    if not delimiter:
        print("Missing '-- [FILES]'")
        sys.exit(1)

    files = sys.argv[delimiter+3:]

    # TODO: How to get those into a single commit? Script in container or
    # call a loop directly?
    for f in files:
        dataset.containers_run(
                ['fslroi', f, f] + params,
                sidecar=False,
                container_name=op.relpath(
                    op.join(op.dirname(op.realpath(__file__)), "fsl.simg"),
                    dataset.path),
                inputs=[f],
                outputs=[f],
                explicit=True,
                expand="both",
        )
