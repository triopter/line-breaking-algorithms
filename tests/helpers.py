from importlib import import_module


def make_algo_id(algo_path):
    return algo_path.stem


def import_algo(algo_name):
    return import_module(f"algorithms.{algo_name}")
