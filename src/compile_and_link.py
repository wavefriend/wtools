import compile
import link

def compile_and_link(cpp_version: int, shared: bool, static: bool, \
                     src_dir_path: str, include_dir_paths: list, lib_names: list, lib_dir_paths: list, \
                     build_dir_path: str, target_path: str) -> None:

    o_changed = compile.compile(cpp_version, src_dir_path, include_dir_paths, build_dir_path)

    link.link(cpp_version, shared, static, lib_names, lib_dir_paths, build_dir_path, target_path, o_changed)