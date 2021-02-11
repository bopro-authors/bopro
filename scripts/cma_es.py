import sys
import os
import space
import numpy as np
import datetime
import cma
import contextlib
import copy
import random

from local_search import get_min_configurations
from utility_functions import *

def cma_es(
            param_space,
            data_array,
            fast_addressing_of_data_array,
            optimization_objective,
            logfile,
            optimization_function,
            optimization_function_parameters,
            cma_es_random_points=10000,
            cma_es_starting_points=10,
            sigma=0.001):
    """
    Optimize the acquisition function using a mix of random and local search.
    This algorithm random samples N points and then does a local search on the
    best points from the random search and the best points from previous iterations (if any).
    :param local_search_starting_points: an integer for the number of starting points for the local search. If 0, all points will be used.
    :param local_search_random_points: number of random points to sample before the local search.
    :param param_space: a space object containing the search space.
    :param fast_addressing_of_data_array: A list containing the points that were already explored.
    :param enable_feasible_predictor: whether to use constrained optimization.
    :param optimization_function: the function that will be optimized by the local search.
    :param optimization_function_parameters: a dictionary containing the parameters that will be passed to the optimization function.
    :param optimization_objective: the name given to the scalarized values.
    :param previous_points: previous points that have already been evaluated.
    :return: all points evaluted and the best point found by the local search.
    """
    t0 = datetime.datetime.now()
    input_params = param_space.get_input_parameters()
    input_param_objects = param_space.get_input_parameters_objects()
    tmp_fast_addressing_of_data_array = copy.deepcopy(fast_addressing_of_data_array)

    # CMA-ES works better if optimizing between normalized ranges
    param_min, param_max = {}, {}
    normalizer = {}
    unnormalizer = {}
    for param in input_params:
        param_min[param], param_max[param] = input_param_objects[param].get_min(), input_param_objects[param].get_max()
        normalizer[param] = lambda x, input_param: (x - param_min[input_param])/(param_max[input_param] - param_min[input_param])
        unnormalizer[param] = lambda x, input_param: x*(param_max[input_param] - param_min[input_param]) + param_min[input_param]

    best_previous = get_min_configurations(
                                        data_array,
                                        cma_es_starting_points,
                                        optimization_objective)

    concatenation_keys = input_params
    cma_es_configurations = {}
    cma_es_configurations = concatenate_data_dictionaries(cma_es_configurations, best_previous, concatenation_keys)
    # Get mode or random
    param_mean = {}
    if param_space.estimate_multivariate_gaussian:
        mean = param_space.mv_mean
        for idx, param in enumerate(input_params):
            param_mean[param] = mean[idx]
            param_mean[param] = [param_mean[param]]
    else:
        for param in input_params:
            param_mean[param] = input_param_objects[param].custom_gaussian_prior_mean
            if param_mean[param] is None:
                param_mean[param] = input_param_objects[param].randomly_select()
            else:
                if type(param_mean[param]) == list:
                    sample_idx = random.randint(0, len(param_mean[param])-1)
                    param_mean[param] = param_mean[param][sample_idx]
            param_mean[param] = [param_mean[param]]

    cma_es_configurations = concatenate_data_dictionaries(cma_es_configurations, param_mean, concatenation_keys)

    # Passing the dictionary with ** expands the key-value pairs into function parameters
    # The acquisition functions return a tuple with two lists, cma wants only the first element of the first list
    cmaes_black_box = lambda x: optimization_function(configurations=[{param: unnormalizer[param](x[param_idx], param) for param_idx, param in enumerate(input_params)}], **optimization_function_parameters)[0][0]
    best_points = []
    best_point_vals = []


    for configuration_idx in range(len(cma_es_configurations[list(cma_es_configurations.keys())[0]])):
        x0 = [normalizer[param](cma_es_configurations[param][configuration_idx], param) for param in input_params]
        with open(logfile, "a") as f, contextlib.redirect_stdout(f):
            es = cma.CMAEvolutionStrategy(x0, sigma, {'bounds': [0, 1]})
            es.optimize(cmaes_black_box)

        best_points.append(es.result.xbest)
        best_point_vals.append(es.result.fbest)

    best_configuration_idx = np.argmin(best_point_vals)
    best_configuration = {param: unnormalizer[param](best_points[best_configuration_idx][param_idx], param) for param_idx, param in enumerate(input_params)}
    configuration_string = param_space.get_unique_hash_string_from_values(best_configuration)
    # If the best configuration has already been evaluated before, remove it and get the next best configuration
    if configuration_string in fast_addressing_of_data_array:
        del best_point_vals[best_configuration_idx]
        del best_points[best_configuration_idx]
        best_configuration_idx = np.argmin(best_point_vals)
        best_configuration = {param: unnormalizer[param](best[param_idx], param) for param_idx, param in enumerate(input_params)}
        configuration_string = param_space.get_unique_hash_string_from_values(best_configuration)

    sys.stdout.write_to_logfile(("CMA-ES time %10.4f sec\n" % ((datetime.datetime.now() - t0).total_seconds())))

    return best_configuration
