# How to run BOPrO

## Installation

BOPrO requires python3. To setup BOPrO, install python3, pip, and then install BOPrO's dependencies with:
```
pip3 install -r requirements.txt
```

## Running BOPrO

The code for the benchmarks used in the paper is provided in the 'benchmarks/' directory. Instructions to run each benchmark are detailed below. By default, BOPrO will use the strong prior centered near the optima. To use the weaker prior, change the value of the "custom_gaussian_prior_stds" field in the benchmark's json file.

### Running the Branin benchmark

The code for running the Branin benchmark used in the paper is provided in the benchmarks/ directory. To run Branin, use:

```
python3 benchmarks/branin/branin.py
```

The benchmark should be executed from the BOPrO root folder. The optimization result will be saved in the "branin_output_samples.csv" file.

### Running the Profet benchmarks

The Profet benchmarks require the Profet data and code. Move to the benchmarks/profet directory and clone the Profet branch from emukit:

```
cd benchmarks/profet
git clone -b profet https://github.com/aaronkl/emukit.git
```

Then, download and extract the data from http://www.automl.org/wp-content/uploads/2019/05/profet_data.tar.gz:

```
wget http://www.automl.org/wp-content/uploads/2019/05/profet_data.tar.gz
tar -xvzf profet_data.tar.gz
cd ../../
```

The profet_data folder that was downloaded should be stored in the benchmarks/profet/ directory. Finally, run one of the benchmarks with one of:

```
python3 benchmarks/profet/svm.py
python3 benchmarks/profet/fcnet.py
python3 benchmarks/profet/xgboost.py
```

All benchmarks should be executed from the BOPrO root folder. The optimization result will be saved in the "[benchmark]\_42\_output\_samples.csv" file.

### Additional Experiments 

#### Multivariate Prior Comparison

To run BOPrO with strong univariate KDE priors, change the "prior" field for each parameter in the benchmark's json file to "estimate". 
To run BOPrO with weak univariate KDE priors, change the "prior" field in the benchmark's json file to "estimate" and the "prior_estimation_file" field to "prior_data/[benchmark]\_weak\_prior". 
To use multivariate KDE priors instead, add the field ```estimate_multivariate_priors=true```

#### Misleading Prior Comparison

To run BOPrO without priors, change the "prior" field for each parameter in the benchmark's json file to "uniform". 
To run BOPrO with our misleading priors, change the "custom\_gaussian\_prior\_mean" field to one of the following:

```
Branin: [-4.999276789971868, 0.001994065426049721]

SVM: [0.37745836069849137, 0.9999636261160244\]

FCNet: [0.09502232195034295, 0.9997423348628324, 0.3849647423269124, 0.9997772780662821, 0.14390988891905773, 0.04496688040264126\]

XGBoost: [0.8430779543903044,0.006946376200865814,0.5745414651554107,0.9917434866272964,0.003974654114357259,0.6004521583282724,0.0028723652870462253,0.9213105105121868]
```

Which correspond to the worst points out of $10,000,000D$ uniform random samples for each benchmark.

#### Forgetting Experiments

To run BOPrO with exponential or decay priors, change the "prior" field for each parameter in the benchmark's json file to either "decay" or "exponential". 
