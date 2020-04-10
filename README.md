# HPA image-distance study on malignant transformation

## Setup

1. configure credentials

    Create file `config.py` in repo top-level containing a dictionary
    `config` that contains mongo, s3, and nferx credentials

2. start docker environment

    prerequisites:

    * docker
    * nvidia-docker

    ```sh
    cd docker && make bash
    ```

## Components

* `utils`: modules
* `notebooks`: experiments
* `docker`: image processing compute environment


## See also

[design doc](https://paper.dropbox.com/doc/Malignant-Transformation-Image-Distance-Study-HPA-data--Ax2iw3CHqFmt9Pe~bBRgho38AQ-VL2CXt7TTbYTml7TI5UIY)