import ast
import py_compile
import tempfile
import os

def check_syntax(code_string):
    try:
        ast.parse(code_string)
        return True, None
    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Parse error: {str(e)}"

def check_compile(code_string):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code_string)
            temp_file = f.name
        
        py_compile.compile(temp_file, doraise=True)
        os.unlink(temp_file)
        return True, None
    except py_compile.PyCompileError as e:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        return False, str(e)
    except Exception as e:
        if os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except:
                pass
        return False, f"Compile error: {str(e)}"

def validate_syntax(code_string):
    syntax_ok, syntax_error = check_syntax(code_string)
    if not syntax_ok:
        return False, "syntax", syntax_error
    
    compile_ok, compile_error = check_compile(code_string)
    if not compile_ok:
        return False, "compile", compile_error
    
    return True, None, None

