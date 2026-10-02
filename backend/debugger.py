import sys
import io
import traceback
import copy
from typing import List, Dict, Any

def run_debug_trace(code: str, input_data: str, max_steps: int = 2000) -> dict:
    """
    Chạy mã Python và ghi lại dấu vết (trace) từng bước thực thi.
    Giới hạn tối đa max_steps để tránh vòng lặp vô hạn.
    """
    steps = []
    
    # Chuẩn bị môi trường stdin/stdout ảo
    old_stdout = sys.stdout
    old_stdin = sys.stdin
    mock_stdout = io.StringIO()
    mock_stdin = io.StringIO(input_data)
    
    sys.stdout = mock_stdout
    sys.stdin = mock_stdin
    
    step_count = 0
    error_msg = None
    
    def trace_lines(frame, event, arg):
        nonlocal step_count, error_msg
        
        # Chỉ theo dõi code được biên dịch từ <string> (code của người dùng)
        if frame.f_code.co_filename != '<string>':
            return trace_lines
            
        if event == 'line':
            step_count += 1
            if step_count > max_steps:
                error_msg = f"Đã vượt quá giới hạn {max_steps} bước chạy. Có thể bạn đang bị lặp vô tận (infinite loop)."
                raise RuntimeError("Max steps exceeded")
                
            # Lọc các biến cục bộ, bỏ qua các biến đặc biệt (__name__, __builtins__...)
            locs = {}
            for k, v in frame.f_locals.items():
                if not k.startswith('__'):
                    # Chuyển đổi an toàn sang chuỗi để tránh lỗi serialize JSON
                    try:
                        locs[k] = repr(v)
                    except Exception:
                        locs[k] = "<unrepresentable>"
            
            steps.append({
                'line': frame.f_lineno,
                'locals': locs,
                'stdout': mock_stdout.getvalue()
            })
            
        return trace_lines

    try:
        compiled_code = compile(code, '<string>', 'exec')
        sys.settrace(trace_lines)
        
        # Thực thi với không gian tên rỗng (mô phỏng môi trường độc lập)
        exec(compiled_code, {})
        
        status = "success"
    except Exception as e:
        status = "error"
        if error_msg:
            err_str = error_msg
        else:
            # Lấy thông tin lỗi
            err_type = type(e).__name__
            err_details = str(e)
            
            # Cố gắng tìm dòng gây lỗi
            tb = traceback.extract_tb(sys.exc_info()[2])
            line_no = None
            for frame in tb:
                if frame.filename == '<string>':
                    line_no = frame.lineno
                    break
            
            if line_no:
                err_str = f"Lỗi {err_type} tại dòng {line_no}: {err_details}"
            else:
                err_str = f"Lỗi {err_type}: {err_details}"
                
        error_msg = err_str
    finally:
        sys.settrace(None)
        sys.stdout = old_stdout
        sys.stdin = old_stdin
        
    return {
        "status": status,
        "error": error_msg,
        "steps": steps,
        "final_stdout": mock_stdout.getvalue()
    }
