# build and run docker image

# ---- PARAMS ----
# FSIO
DATA?="$/datastorage"
HDD?="/datastorage"
SRC?=$(shell dirname `pwd`)

# CONFIG
GPU?=0
DOCKER_FILE=Dockerfile
#! no longer need nvidia-docker with docker version 19.03+
#DOCKER=GPU=$(GPU) nvidia-docker
DOCKER=docker
BACKEND=tensorflow
PYTHON_VERSION?=3.6
CUDA_VERSION?=9.0
CUDNN_VERSION?=7
IMAGE_TAG=deep_path 
CLIENT_PORT=8888


# ---- RECIPES ----
help:
	@cat Makefile

build:
	@echo Build an image from a Dockerfile
	docker build -t $(IMAGE_TAG) --build-arg python_version=$(PYTHON_VERSION) --build-arg cuda_version=$(CUDA_VERSION) --build-arg cudnn_version=$(CUDNN_VERSION) -f $(DOCKER_FILE) .
	# 			 ^ name the resulting image's repo
	# 			 		  ^ name and value for a buildarg - a variable set in a Dockerfile with the directive `ARG`

show:
	docker images

clean:
	docker image rm $(IMAGE_TAG)


# docker-run methods: each recipe launches docker with a distinct process (e.g., bash, ipython, jupyter notebook)
# synopsis: docker run [options] IMAGE [COMMAND] [ARG...]
# the key distinction between these recipes is the COMMAND
bash: build
	$(DOCKER) run -it -u root -v $(SRC):/src/workspace -v $(DATA):/data -v $(HDD):/data/hdd --env KERAS_BACKEND=$(BACKEND) $(IMAGE_TAG) bash
	#					      ^ create a bind mount from host-dir SRC to container-dir /src/workspace
	#																						         							 ^ command "bash"
	
ipython: build
	$(DOCKER) run -it -v $(SRC):/src/workspace -v $(DATA):/data -v $(HDD):/data/hdd --env KERAS_BACKEND=$(BACKEND) $(IMAGE_TAG) ipython

notebook: build
	@echo launching notebook forwarded to 'localhost:8484'
	$(DOCKER) run -it -p $(CLIENT_PORT):8888 --workdir="/src/workspace" -v $(SRC):/src/workspace -v $(DATA):/data -v $(HDD):/data/hdd --net=host --env KERAS_BACKEND=$(BACKEND) $(IMAGE_TAG)
	#		  ^ bind docker port 8888 to localhost port 8484
	#		                         ^ set workdir to root of container so all contents can be accessed in jupyter GUI
	# no COMMAND b/c image has the default `CMD jupyter notebook`
	
