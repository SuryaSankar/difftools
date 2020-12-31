"""Main module."""
from git import Repo
import io
import ast
import difflib
from toolspy.collection_tools import intersection


def file_handle_from_git_ref(repo_path, relative_file_path, branch_name="master"):
    repo = Repo.init(repo_path)
    tree = repo.heads[branch_name].commit.tree
    blob = tree[relative_file_path]
    return io.TextIOWrapper(io.BytesIO(blob.data_stream.read()))

def source_code_from_git_ref(repo_path, relative_file_path, branch_name="master"):
    return file_handle_from_git_ref(
        repo_path, relative_file_path, branch_name=branch_name).read()

def ast_from_git_ref(repo_path, relative_file_path, branch_name="master"):
    return ast.parse(source_code_from_git_ref(
        repo_path, relative_file_path, branch_name=branch_name
    ))

def function_names_to_ast_nodes_map(ast_tree):
    return {n.name: n for n in ast_tree.body if isinstance(n, ast.FunctionDef)}

def function_names_to_source_segments_map(ast_tree, source_code):
    return {
        n.name: ast.get_source_segment(source_code, n) 
        for n in ast_tree.body if isinstance(n, ast.FunctionDef)
    }

def function_names_to_ast_nodes_map_from_git_ref(
        repo_path, relative_file_path, branch_name="master"):
    return function_names_to_ast_nodes_map(ast_from_git_ref(
        repo_path, relative_file_path, branch_name=branch_name
    ))

def function_names_to_source_segments_map_from_git_ref(
        repo_path, relative_file_path, branch_name="master"):
    source_code = source_code_from_git_ref(
        repo_path, relative_file_path, branch_name=branch_name
    )
    ast_tree = ast.parse(source_code)
    return function_names_to_source_segments_map(ast_tree, source_code)

def common_but_differing_functions_mapped_to_ast_nodes(repo_path, fileref1, fileref2):
    branch1, filepath1 = fileref1.split(":")
    branch2, filepath2 = fileref2.split(":")
    funcs_to_nodes_map_1 = function_names_to_ast_nodes_map_from_git_ref(
        repo_path, filepath1, branch_name=branch1
    )
    funcs_to_nodes_map_2 = function_names_to_ast_nodes_map_from_git_ref(
        repo_path, filepath2, branch_name=branch2
    )
    common_funcs = intersection([funcs_to_nodes_map_1.keys(), funcs_to_nodes_map_2.keys()])
    return {
        fn: {
            fileref1: funcs_to_nodes_map_1[fn],
            fileref2: funcs_to_nodes_map_2[fn]
        }
        for fn in common_funcs
        if ast.dump(funcs_to_nodes_map_1[fn]) != ast.dump(funcs_to_nodes_map_2[fn])
    }

def common_but_differing_functions_mapped_to_source_codes(repo_path, fileref1, fileref2):
    branch1, filepath1 = fileref1.split(":")
    branch2, filepath2 = fileref2.split(":")
    funcs_to_source_codes_map_1 = function_names_to_source_segments_map_from_git_ref(
        repo_path, filepath1, branch_name=branch1
    )
    funcs_to_source_codes_map_2 = function_names_to_source_segments_map_from_git_ref(
        repo_path, filepath2, branch_name=branch2
    )
    common_funcs = intersection([funcs_to_source_codes_map_1.keys(), funcs_to_source_codes_map_2.keys()])
    return {
        fn: {
            fileref1: funcs_to_source_codes_map_1[fn],
            fileref2: funcs_to_source_codes_map_2[fn]
        }
        for fn in common_funcs
        if funcs_to_source_codes_map_1[fn] != funcs_to_source_codes_map_2[fn]
    }

def print_diffs_map(diffs_map):
    for k, v in diffs_map.items():
        print(k)
        print("".join(v))
        print()

def diffs_of_common_functions(repo_path, fileref1, fileref2, print_diffs=False):
    funcs_sources_map = common_but_differing_functions_mapped_to_source_codes(
        repo_path, fileref1, fileref2)
    result = {
        fn: list(difflib.unified_diff(
            funcs_sources_map[fn][fileref1].splitlines(1),
            funcs_sources_map[fn][fileref2].splitlines(1),
            fromfile=fileref1,
            tofile=fileref2
        ))
        for fn in funcs_sources_map.keys()
    }
    if print_diffs:
        print_diffs_map(result)
    return result






