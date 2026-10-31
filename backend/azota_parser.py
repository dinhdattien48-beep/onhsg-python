"""
azota_parser.py - Bộ phân tích đề thi trắc nghiệm chuẩn Azota.
Hỗ trợ cả file Word (.docx) và văn bản thuần túy (Text/Paste).
Tự động nhận diện câu hỏi, các phương án A, B, C, D, đáp án đúng (gạch chân / in đậm / bảng đáp án cuối đề)
và lời giải chi tiết.
"""

import io
import re
from typing import Dict, List, Any, Optional

try:
    import docx
except ImportError:
    docx = None


def parse_azota_text(raw_text: str) -> Dict[str, Any]:
    """
    Phân tích đề thi từ chuỗi văn bản thô (paste từ Word hoặc gõ trực tiếp).
    """
    if not raw_text or not raw_text.strip():
        return {"success": False, "total_questions": 0, "questions": [], "error": "Văn bản rỗng."}

    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    
    # 1. Tìm bảng đáp án ở cuối đề (nếu có)
    # Ví dụ: "ĐÁP ÁN: 1.A 2.B 3.C 4.D" hoặc "1-A, 2-B, 3-C"
    end_answers = {}
    end_answers_start_idx = -1
    
    for i, line in enumerate(lines):
        if re.search(r'^(?:B[ẢAảa]NG\s+)?(?:Đ[ÁáaA]|D[ÁáaA])\s*[PPAp]\s*(?:[ÁáaA]N|[ÀàaA]N)(?:\s*TR[ẮAắa]C\s*NGHI[ỆEệe]M)?[:\s]*$', line, re.IGNORECASE):
            end_answers_start_idx = i
            break
            
    if end_answers_start_idx != -1:
        answer_text = " ".join(lines[end_answers_start_idx:])
        # Bắt các cặp "1.A", "1-A", "1: A", "Câu 1: A", "1A", "1. A"
        matches = re.findall(r'(?:(?:C[ÂâaAuU]{1,3}|B[àaA]i)\s*)?(\d+)\s*[\.\-:\)]?\s*([A-D])\b', answer_text, re.IGNORECASE)
        for q_num, ans in matches:
            end_answers[int(q_num)] = ans.upper()
        # Cắt bỏ phần bảng đáp án khỏi nội dung câu hỏi
        lines = lines[:end_answers_start_idx]

    # 2. Gom và tách các câu hỏi
    # Nhận diện đầu câu: "Câu 1:", "Câu 1.", "Câu 1", "CÂU 1", "Cau 1:", "Bài 1:", hoặc "1.", "1:"
    q_start_regex = re.compile(
        r'^(?:(?:C[ÂâaAuU]{1,3}|B[àaA]i)\s*)?(\d+)[\.:\)\s\-]+(.*)$',
        re.IGNORECASE
    )
    
    questions: List[Dict[str, Any]] = []
    current_q: Optional[Dict[str, Any]] = None

    def finalize_current_q():
        nonlocal current_q
        if not current_q:
            return
        
        # Ghép các dòng của câu hiện tại
        full_text = "\n".join(current_q["_raw_lines"]).strip()
        if not full_text:
            return
        
        # Tách phần câu hỏi, các phương án, và lời giải
        explanation = ""
        exp_match = re.search(
            r'(?:Lời\s*giải|Hướng\s*dẫn\s*giải|Giải\s*thích|Giải|Loi\s*giai)[:\s]+([\s\S]*)$',
            full_text, re.IGNORECASE
        )
        if exp_match:
            explanation = exp_match.group(1).strip()
            full_text = full_text[:exp_match.start()].strip()
            
        # Tìm xem có dòng "Đáp án: A" hay không
        inline_ans_match = re.search(
            r'(?:Đáp\s*án|Đ/A|Dap\s*an|Chọn|Chon|Answer)[:\s]+([A-D])\b',
            full_text, re.IGNORECASE
        )
        inline_ans = inline_ans_match.group(1).upper() if inline_ans_match else None
        if inline_ans_match:
            full_text = full_text[:inline_ans_match.start()].strip()

        # Tìm các phương án A, B, C, D (hỗ trợ cả dòng đơn lẫn nằm chung dòng)
        opt_matches = list(re.finditer(
            r'(?:^|[\r\n\t]|\s{2,})([A-D])[\.\:\)]\s*',
            full_text, re.MULTILINE
        ))
        
        if len(opt_matches) >= 2:
            q_title = full_text[:opt_matches[0].start()].strip()
            # Bỏ tiền tố "Câu 1:" khỏi tiêu đề nếu còn
            q_title = re.sub(r'^(?:(?:C[ÂâaAuU]{1,3}|B[àaA]i)\s*)?\d+[\.:\)\s\-]+', '', q_title).strip()
            if not q_title:
                q_title = full_text[:opt_matches[0].start()].strip()

            options = []
            opt_labels = []
            for j in range(len(opt_matches)):
                start = opt_matches[j].end()
                end = opt_matches[j + 1].start() if j + 1 < len(opt_matches) else len(full_text)
                opt_text = full_text[start:end].strip()
                options.append(opt_text)
                opt_labels.append(opt_matches[j].group(1).upper())

            # Xác định đáp án đúng
            ans_idx = None
            q_num = current_q["id"]
            
            # Ưu tiên 1: Đánh dấu inline "Đáp án: A"
            # Ưu tiên 2: Bảng đáp án cuối đề
            # Ưu tiên 3: Gạch chân / in đậm từ docx (nếu có)
            target_char = inline_ans or end_answers.get(q_num)
            if not target_char and current_q.get("_detected_char"):
                target_char = current_q["_detected_char"]

            if target_char:
                target_char = target_char.upper()
                if target_char in opt_labels:
                    ans_idx = opt_labels.index(target_char)
                else:
                    ans_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
                    ans_idx = ans_map.get(target_char, 0)
            
            questions.append({
                "id": len(questions) + 1,
                "original_id": q_num,
                "question": q_title,
                "options": options,
                "answer": ans_idx,  # 0, 1, 2, 3 hoặc null nếu chưa có
                "explanation": explanation
            })

    for line in lines:
        # Kiểm tra xem dòng có phải là bắt đầu câu mới không
        # Lưu ý: Không nhầm lẫn với phương án "A. ...", "B. ..."
        is_opt_line = re.match(r'^[A-D][\.\:\)]\s*', line, re.IGNORECASE)
        m = q_start_regex.match(line) if not is_opt_line else None
        
        # Chỉ coi là câu mới nếu có chữ "Câu", "Bài" hoặc số thứ tự tăng dần
        if m and (re.search(r'(?:C[ÂâaAuU]{1,3}|B[àaA]i)', line, re.IGNORECASE) or int(m.group(1)) == (len(questions) + 1)):
            finalize_current_q()
            q_num = int(m.group(1))
            current_q = {
                "id": q_num,
                "_raw_lines": [line],
                "_detected_char": None
            }
        else:
            if current_q:
                current_q["_raw_lines"].append(line)

    finalize_current_q()

    return {
        "success": True,
        "total_questions": len(questions),
        "questions": questions
    }


def parse_azota_docx(file_bytes: bytes) -> Dict[str, Any]:
    """
    Phân tích đề thi trực tiếp từ file Word (.docx) của giáo viên.
    Trích xuất text, nhận diện đáp án gạch chân / in đậm (chuẩn Azota).
    """
    if not docx:
        return {"success": False, "error": "Thư viện python-docx chưa được cài đặt."}

    doc = docx.Document(io.BytesIO(file_bytes))
    
    # Ghép văn bản với các đánh dấu gạch chân đặc biệt để nhận diện đáp án đúng
    # Nếu một run có underline, gắn thẻ [U]...[/U]
    processed_paragraphs = []
    
    for p in doc.paragraphs:
        p_text_parts = []
        for r in p.runs:
            t = r.text
            if not t:
                continue
            # Chuẩn Azota: Gạch chân chữ cái đáp án (A, B, C, D)
            if r.underline:
                t = f"[U]{t}[/U]"
            p_text_parts.append(t)
        
        line = "".join(p_text_parts).strip()
        if line:
            processed_paragraphs.append(line)

    raw_text = "\n".join(processed_paragraphs)
    
    # Tìm xem phương án nào có [U]A[/U] hoặc [U]A.[/U]
    underlined_answers = {}
    lines = raw_text.splitlines()
    
    current_q_num = None
    q_start_regex = re.compile(r'^(?:(?:C[ÂâaAuU]{1,3}|B[àaA]i)\s*)?(\d+)[\.:\)\s\-]+', re.IGNORECASE)
    
    for line in lines:
        is_opt = re.match(r'^(?:\[U\])?[A-D][\.\:\)]?', line, re.IGNORECASE)
        qm = q_start_regex.match(line) if not is_opt else None
        if qm and re.search(r'(?:C[ÂâaAuU]{1,3}|B[àaA]i)', line, re.IGNORECASE):
            current_q_num = int(qm.group(1))
            
        if current_q_num:
            # Tìm [U]A[/U] hoặc [U]B[/U]...
            u_match = re.search(r'\[U\]\s*([A-D])[\.\:\)]?\s*\[/U\]', line, re.IGNORECASE)
            if u_match:
                underlined_answers[current_q_num] = u_match.group(1).upper()
            else:
                # Trường hợp gạch chân cả cụm đáp án: [U]A. Hà Nội[/U]
                u_full = re.search(r'\[U\]\s*([A-D])[\.\:\)]', line, re.IGNORECASE)
                if u_full:
                    underlined_answers[current_q_num] = u_full.group(1).upper()

    # Bỏ các thẻ [U] và [/U] để đưa về text sạch
    clean_text = re.sub(r'\[/?U\]', '', raw_text)
    
    result = parse_azota_text(clean_text)
    
    # Gán lại các đáp án được phát hiện từ gạch chân Word nếu chưa có
    for q in result.get("questions", []):
        q_id = q.get("original_id") or q.get("id")
        if q["answer"] is None and q_id in underlined_answers:
            char = underlined_answers[q_id]
            ans_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
            q["answer"] = ans_map.get(char, 0)
            
    return result
