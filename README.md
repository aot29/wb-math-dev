A development environment for Mediawiki and Wikibase
* [Mediawiki 1.38](https://gerrit.wikimedia.org/r/mediawiki/core.git) included as a submodule
* Python tools for data science and Jupyter notebooks

Clone this repo and all submodules
`git clone --recurse-submodules git@github.com:aot29/wb-math-dev.git`

## Prerequisites
* [Docker](https://docs.docker.com/engine/install/), [docker-compose](https://docs.docker.com/compose/install/)
* Python3
* [Anaconda](https://docs.continuum.io/anaconda/install/) (recommended)

Re-open the shell, or login again for changes to take effect

Create a new Python environment
cd path-to-this-repo
`conda env create -f wb-math-dev.yml`
This will install
* basic data and plotting packages: matplotlib, numpy, pandas, seaborn
* data science packages: scikit-learn, scipy, tensorflow, nltk
* Jupyter notebooks
* utilities: invoke, requests, lxml, etc.

Activate the environmanet
`conda activate wb-math-dev`

Start Jupyter notebooks (optional)
`jupyter lab` (close with Ctrl-C)

## Installation
Make sure the Conda environment is activated
`conda activate wb-math-dev`

Run the Mediawiki installation script
`invoke mwInstall` and set the Admin password for your installation.
Wait for everything to start

Run the Mediawiki post-installation script
`invoke mwPostInstall`
