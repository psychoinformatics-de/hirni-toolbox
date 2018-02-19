# Singularity recipe for CBBS ' data conversion container
#
# This is based on neurodebian's recipe and under heavy development.

BootStrap: debootstrap
OSVersion: stretch
MirrorURL: http://http.debian.net/debian/

%setup
    set -eu
    echo "Setting up the environment"
    #apt-get update
    #apt-get -y install python 


    # TODO: Probably not needed:
    v=`git describe --tags --match sing-\* | sed -e 's,^sing-,,g'`; \
      python -c "import json, os; f='$SINGULARITY_ROOTFS/.singularity.d/labels.json'; j=json.load(open(f)) if os.path.exists(f) else {}; j['SINGULARITY_IMAGE_VERSION']='$v' or '0.0.unknown'; json.dump(j, open(f,'w'),indent=2)"
    chmod a+r "$SINGULARITY_ROOTFS/.singularity.d/labels.json"
    mkdir -p ${SINGULARITY_ROOTFS}/cbbs-container-code

%files
code/*.sh /cbbs-container-code/
code/*.py /cbbs-container-code/

%help

Singularity container to run CBBS' raw data import/conversion tools in.
TODO: Proper CBBS acknowledgement


%post
    echo "Configuring the environment"
    sed -i -e 's, main$, main contrib non-free,g' /etc/apt/sources.list
    # For build-dep
    # sed -i -e 's,^deb \(.*\),deb \1\ndeb-src \1,g' /etc/apt/sources.list
    apt-get update
    apt-get -y install eatmydata 
    eatmydata apt-get -y install vim wget time gnupg curl procps
    # eatmydata apt-get -y build-dep git
    wget -q -O/tmp/nd-configurerepo https://raw.githubusercontent.com/neurodebian/neurodebian/4d26c8f30433145009aa3f74516da12f560a5a13/tools/nd-configurerepo
    bash /tmp/nd-configurerepo
    chmod a+r -R /etc/apt
    eatmydata apt-get -y install git git-annex-standalone virtualenv dcm2niix python-dcmstack python-configparser python-funcsigs python-pytest python-pip python3-pip python-lzma

    # for bids-validator
    # curl -sL https://deb.nodesource.com/setup_6.x | bash - && \
    #    eatmydata apt-get install -y nodejs
    # npm install -g bids-validator@0.22.0
    # chmod a+rX -R /usr/lib/node_modules/

    chmod a+rX -R /etc/apt/sources.list.d
    # cleaning /tmp that thoroughly might have side effects 
    # rm -rf /tmp/* /var/tmp/*
    rm -rf /tmp/npm-* /tmp/nd-config* /tmp/startup* /var/tmp/npm-*
    apt-get clean

    # and wipe out apt lists since not to be used RW for further tuning
    # find /var/lib/apt/lists/ -type f -delete
    # /usr/bin/find /var/lib/apt/lists/ -type f -name \*Packages\* -o -name \*Contents\*
    # complicates later interrogation - thus disabled

    # Create some additional bind mount directories present on various compute boxes we have
    # access to, to ease deployment
    # mkdir -p /afs /inbox /ihome /opt /data /backup /apps /srv /scratch /idata
    # chmod a+rX /afs /inbox /ihome /opt /data /backup /apps /srv /scratch /idata

    pip install cili
    pip install numpy


    # -------------->
    pip install git+https://github.com/datalad/datalad@master


    pip install git+https://github.com/bpoldrack/heudiconv@cbbs-imaging
    # actually install scripts from /code (see %files):
    install cbbs-container-code/* /usr/local/bin

# --------------->
%runscript
    case "$1" in
        create)
            exec create_study_ds.sh "$2"
            ;;
        import)
            exec add_scan_tarball.sh "$2"
            ;;
         
        dicom2bids)
            exec convert_dicom_ds.sh "$2" "$3"
            ;;
         
        *)
            echo $"Usage: $0 {create [TARGET_DIR]|import ABS_PATH_TO_TARBALL|dicoms2bids SUBDATASET TARGET_DIR}"
            exit 1
    esac
    
