from .io_utils import write_json, ensure_dir

def dump_metric(path, **kwargs):
    write_json(path, kwargs)
