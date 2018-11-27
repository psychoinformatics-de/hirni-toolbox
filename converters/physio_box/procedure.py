if __name__ == '__main__':

    # arguments:
    # dataset
    # anonymize
    # + arguments for convert_physio_box.py

    import sys
    import os.path as op
    from datalad.api import Dataset
    from datalad.config import anything2bool

    dataset = Dataset(sys.argv[1])
    converter_path = op.join(op.dirname(__file__), 'convert_physio_box.py')
    anonymize = anything2bool(sys.argv[2])
    arguments = " ".join(sys.argv[3:])
    input_file = sys.argv[3]
    call = "{conv} {args}".format(conv=converter_path, args=arguments)
    print("DEBUG:\ncall: %s\ninputs: %s" % (call, input_file))
    dataset.run(call,
                sidecar=anonymize,
                inputs=[input_file],
                outputs=[dataset.path],
                message="[HIRNI] Convert physio box file")
