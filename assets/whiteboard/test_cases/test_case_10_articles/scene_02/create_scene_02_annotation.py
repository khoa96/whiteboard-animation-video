#!/usr/bin/env python3
"""
Sinh file annotation.json chuẩn cho Scene 02 (Test Case 10: Articles - Vowels and Consonants)
- Canvas: 1920x1080, Nền trắng thuần #FFFFFF
- Phân rã nguyên tử 13 vùng (Zero-Overlap 0.00%, Unassigned 0.00%)
- Đồng bộ chuẩn xác theo Audio Master Clock timing_cues.json (Tổng: 33,172 ms)
- Tỉ lệ ink:wash:
  + Chữ tiêu đề và chữ cái phụ âm: colorMode="none" (100% ink)
  + 5 thẻ nguyên âm A E I O U và thẻ Y: colorMode="wash" (viền nét mực trước, đổ màu xanh/cam sau)
"""
from pathlib import Path
import json

DIR = Path(__file__).resolve().parent
ANN_PATH = DIR / "scene_02.annotation.json"

elements = [
    # ---------------- 1. Tiêu đề đỉnh (Sentence 1: 500..4124ms) ----------------
    {
        "id": "el-01-title",
        "label": "Tiêu đề: VOWELS & CONSONANTS",
        "sequence": 1,
        "type": "text",
        "colorMode": "none",
        "narrativeRole": "Giới thiệu nguyên âm và phụ âm trong bảng chữ cái",
        "region": {"x": 450, "y": 60, "width": 1020, "height": 120},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 600,
            "durationMs": 3300,
            "maskPaddingPx": 10,
            "protectedRegions": []
        }
    },

    # ---------------- 2. Nhóm Nguyên âm (Sentence 2: 4624..10096ms) ----------------
    {
        "id": "el-02-vowel-header",
        "label": "Nhãn: VOWEL LETTERS",
        "sequence": 2,
        "type": "text",
        "colorMode": "none",
        "narrativeRole": "Tiêu đề nhóm chữ cái nguyên âm",
        "region": {"x": 120, "y": 240, "width": 640, "height": 100},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 4650,
            "durationMs": 1300,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    {
        "id": "el-03-vowel-a",
        "label": "Chữ cái nguyên âm: A",
        "sequence": 3,
        "type": "colored_image",
        "colorMode": "wash",
        "narrativeRole": "Nguyên âm A (hộp xanh dương)",
        "region": {"x": 100, "y": 365, "width": 130, "height": 135},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 6050,
            "durationMs": 750,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    {
        "id": "el-04-vowel-e",
        "label": "Chữ cái nguyên âm: E",
        "sequence": 4,
        "type": "colored_image",
        "colorMode": "wash",
        "narrativeRole": "Nguyên âm E (hộp xanh dương)",
        "region": {"x": 235, "y": 365, "width": 130, "height": 135},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 6850,
            "durationMs": 750,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    {
        "id": "el-05-vowel-i",
        "label": "Chữ cái nguyên âm: I",
        "sequence": 5,
        "type": "colored_image",
        "colorMode": "wash",
        "narrativeRole": "Nguyên âm I (hộp xanh dương)",
        "region": {"x": 375, "y": 365, "width": 120, "height": 135},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 7650,
            "durationMs": 750,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    {
        "id": "el-06-vowel-o",
        "label": "Chữ cái nguyên âm: O",
        "sequence": 6,
        "type": "colored_image",
        "colorMode": "wash",
        "narrativeRole": "Nguyên âm O (hộp xanh dương)",
        "region": {"x": 505, "y": 365, "width": 130, "height": 135},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 8450,
            "durationMs": 750,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    {
        "id": "el-07-vowel-u",
        "label": "Chữ cái nguyên âm: U",
        "sequence": 7,
        "type": "colored_image",
        "colorMode": "wash",
        "narrativeRole": "Nguyên âm U (hộp xanh dương)",
        "region": {"x": 645, "y": 365, "width": 130, "height": 135},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 9250,
            "durationMs": 800,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },

    # ---------------- 3. Nhóm Phụ âm (Sentence 3: 10596..14844ms) ----------------
    {
        "id": "el-08-consonant-header",
        "label": "Nhãn: CONSONANT LETTERS",
        "sequence": 8,
        "type": "text",
        "colorMode": "none",
        "narrativeRole": "Tiêu đề nhóm chữ cái phụ âm",
        "region": {"x": 980, "y": 240, "width": 840, "height": 100},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 10600,
            "durationMs": 1100,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    {
        "id": "el-09-consonants-r1",
        "label": "Hàng phụ âm 1: B C D F G H J",
        "sequence": 9,
        "type": "text",
        "colorMode": "none",
        "narrativeRole": "Hàng phụ âm thứ nhất",
        "region": {"x": 960, "y": 375, "width": 880, "height": 115},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 11800,
            "durationMs": 950,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    {
        "id": "el-10-consonants-r2",
        "label": "Hàng phụ âm 2: K L M N P Q R",
        "sequence": 10,
        "type": "text",
        "colorMode": "none",
        "narrativeRole": "Hàng phụ âm thứ hai",
        "region": {"x": 960, "y": 510, "width": 880, "height": 115},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 12850,
            "durationMs": 950,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },
    {
        "id": "el-11-consonants-r3",
        "label": "Hàng phụ âm 3: S T V W X Z",
        "sequence": 11,
        "type": "text",
        "colorMode": "none",
        "narrativeRole": "Hàng phụ âm thứ ba",
        "region": {"x": 960, "y": 645, "width": 880, "height": 115},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 13900,
            "durationMs": 900,
            "maskPaddingPx": 6,
            "protectedRegions": []
        }
    },

    # ---------------- 4. Ghi chú chữ Y (Sentence 4: 15344..19976ms) ----------------
    {
        "id": "el-12-note-y-badge",
        "label": "Hộp chữ Y (cam)",
        "sequence": 12,
        "type": "colored_image",
        "colorMode": "wash",
        "narrativeRole": "Chữ cái Y có thể làm nguyên âm",
        "region": {"x": 480, "y": 840, "width": 110, "height": 135},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 15400,
            "durationMs": 1200,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    },
    {
        "id": "el-13-note-y-text",
        "label": "Ghi chú: CAN ALSO BE A VOWEL",
        "sequence": 13,
        "type": "text",
        "colorMode": "none",
        "narrativeRole": "Quy tắc đặc biệt chữ Y",
        "region": {"x": 595, "y": 840, "width": 865, "height": 135},
        "reveal": {
            "direction": "left_to_right",
            "startMs": 16700,
            "durationMs": 3000,
            "maskPaddingPx": 8,
            "protectedRegions": []
        }
    }
]

annotation_data = {
    "sceneId": "test_case_10_scene_02",
    "canvas": {
        "width": 1920,
        "height": 1080
    },
    "storyBasis": "Infographic phân biệt Vowels (A E I O U) và Consonants, kèm ghi chú đặc biệt chữ Y có thể hoạt động như nguyên âm, đặt nền móng cho quy tắc chọn A hay AN theo âm đầu.",
    "sceneDurationMs": 33172,
    "elements": elements
}

with open(ANN_PATH, "w", encoding="utf-8") as f:
    json.dump(annotation_data, f, ensure_ascii=False, indent=2)

print(f"Saved {ANN_PATH} with {len(elements)} elements. Total Duration: {annotation_data['sceneDurationMs']} ms")
