def dict_pop(d, to_pop):
    return {k: v for k, v in d.items() if k not in to_pop}
