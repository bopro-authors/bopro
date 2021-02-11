# How to run BOPrO

## Installation

BOPrO requires python3. To setup BOPrO, install python3, pip, and then install BOPrO's dependencies with:
pip3 install -r requirements.txt

## Running BOPrO

The code for the benchmarks used in the paper is provided in the 'benchmarks/' directory. Instructions to run each benchmark are detailed below. By default, BOPrO will use the strong prior centered near the optima. To use the weaker prior, change the value of the "custom_gaussian_prior_stds" field in the benchmark's json file.

### Running the Branin benchmark

The code for running the Branin benchmark used in the paper is provided in the benchmarks/ directory. To run Branin, use:

python3 benchmarks/branin/branin.py

The benchmark should be executed from the BOPrO root folder. The optimization result will be saved in the "branin_output_samples.csv" file.

### Running the Profet benchmarks

The Profet benchmarks require the Profet data and code. Move to the benchmarks/profet directory and clone the Profet branch from emukit:

cd benchmarks/profet
git clone -b profet https://github.com/aaronkl/emukit.git

Then, download and extract the data from http://www.automl.org/wp-content/uploads/2019/05/profet_data.tar.gz:

wget http://www.automl.org/wp-content/uploads/2019/05/profet_data.tar.gz
tar -xvzf profet_data.tar.gz
cd ../../

The profet_data folder that was downloaded should be stored in the benchmarks/profet/ directory. Finally, run one of the benchmarks with one of:

python3 benchmarks/profet/svm.py
python3 benchmarks/profet/fcnet.py
python3 benchmarks/profet/xgboost.py

All benchmarks should be executed from the BOPrO root folder. The optimization result will be saved in the "[benchmark]_42_output_samples.csv" file.

