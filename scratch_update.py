import sys

file_path = r'C:\Users\TDat\Desktop\KHKT\Onhsg\backend\seed_data.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

md_path = r'C:\Users\TDat\Desktop\KHKT\Onhsg\Ôn TN THPT QGia\LoTrinh_OnThi_THPT_QGia.md'
with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

stage_9_code = f'''
STAGE_9_THEORY = r"""
{md_content}
"""

STAGE_9_WEAPON = r"""
## 🔫 Chú ý:
Phần này tập trung hoàn toàn vào lý thuyết phục vụ kỳ thi Tốt nghiệp THPT Quốc Gia môn Tin học (Định hướng Khoa học Máy tính). Không có bài tập lập trình Python đi kèm.
"""

STAGE_9_PROBLEMS = []
'''

content = content.replace('STAGES = [', stage_9_code + '\nSTAGES = [')

new_stage_dict = '''    {
        "id": 9,
        "title": "Ôn thi Tốt nghiệp THPT QG - CSDL",
        "icon": "🎓",
        "theory": STAGE_9_THEORY,
        "weapon": STAGE_9_WEAPON,
        "problems": STAGE_9_PROBLEMS,
    },
]'''

content = content.replace('    },\n]', new_stage_dict)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
