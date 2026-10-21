import json
from pathlib import Path

ann = {
  "version": "1.0",
  "canvas": {
    "width": 1920,
    "height": 1080
  },
  "sceneDurationMs": 29500,
  "storyBasis": "Countable vs Uncountable Nouns: So sánh danh từ đếm được (1 apple -> 3 apples) và không đếm được (water, rice, milk), cách đo lường lượng (a glass of water, a bowl of rice, a bottle of milk) và câu ví dụ với gạch chân từ 'water'.",
  "elements": [
    # ZONE 1: TITLE & CORE THEMES
    {
      "id": "el-01-title",
      "sequence": 1,
      "label": "Tiêu đề: 1. COUNTABLE vs UNCOUNTABLE",
      "type": "text",
      "narrativeRole": "Giới thiệu chủ đề bài học ngữ pháp",
      "region": {
        "x": 40,
        "y": 55,
        "width": 1820,
        "height": 130
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 400,
        "durationMs": 1600,
        "protectedRegions": []
      }
    },
    {
      "id": "el-02-kw-count",
      "sequence": 2,
      "label": "Từ khóa: COUNT (xanh dương)",
      "type": "text",
      "narrativeRole": "Khái niệm đếm được",
      "region": {
        "x": 520,
        "y": 200,
        "width": 240,
        "height": 80
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 2100,
        "durationMs": 400,
        "protectedRegions": []
      }
    },
    {
      "id": "el-03-kw-quantity",
      "sequence": 3,
      "label": "Từ khóa: QUANTITY (xanh lá)",
      "type": "text",
      "narrativeRole": "Khái niệm số lượng",
      "region": {
        "x": 800,
        "y": 200,
        "width": 320,
        "height": 80
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 2550,
        "durationMs": 450,
        "protectedRegions": []
      }
    },
    {
      "id": "el-04-kw-nouns",
      "sequence": 4,
      "label": "Từ khóa: NOUNS (đen)",
      "type": "text",
      "narrativeRole": "Khái niệm danh từ",
      "region": {
        "x": 1180,
        "y": 200,
        "width": 240,
        "height": 80
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 3050,
        "durationMs": 400,
        "protectedRegions": []
      }
    },
    {
      "id": "el-05-divider-top",
      "sequence": 5,
      "label": "Đường kẻ phân cách Zone 1 và 2",
      "type": "underline",
      "narrativeRole": "Phân chia bố cục bảng trắng",
      "region": {
        "x": 0,
        "y": 288,
        "width": 1920,
        "height": 10
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 3500,
        "durationMs": 600,
        "protectedRegions": []
      }
    },

    # ZONE 2: COUNTABLE (LEFT)
    {
      "id": "el-06-hd-countable",
      "sequence": 6,
      "label": "Tiêu đề nhóm: 2. COUNTABLE",
      "type": "text",
      "narrativeRole": "Bắt đầu nhóm danh từ đếm được",
      "region": {
        "x": 40,
        "y": 320,
        "width": 740,
        "height": 105
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 4200,
        "durationMs": 800,
        "protectedRegions": []
      }
    },
    {
      "id": "el-07-one-apple",
      "sequence": 7,
      "label": "Hình vẽ: 1 quả táo đỏ",
      "type": "colored_image",
      "narrativeRole": "Minh họa đơn vị số ít",
      "region": {
        "x": 200,
        "y": 360,
        "width": 210,
        "height": 190
      },
      "reveal": {
        "direction": "radial_outward",
        "startMs": 5100,
        "durationMs": 1100,
        "protectedRegions": []
      }
    },
    {
      "id": "el-08-label-1apple",
      "sequence": 8,
      "label": "Nhãn: 1 apple",
      "type": "text",
      "narrativeRole": "Ghi chú số lượng 1 quả",
      "region": {
        "x": 180,
        "y": 555,
        "width": 260,
        "height": 90
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 6250,
        "durationMs": 500,
        "protectedRegions": []
      }
    },
    {
      "id": "el-09-arrow-trans",
      "sequence": 9,
      "label": "Mũi tên chuyển đổi xanh dương (1 -> 3)",
      "type": "colored_image",
      "narrativeRole": "Chuyển đổi số ít sang số nhiều",
      "region": {
        "x": 430,
        "y": 440,
        "width": 140,
        "height": 100
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 6800,
        "durationMs": 500,
        "protectedRegions": []
      }
    },
    {
      "id": "el-10-three-apples",
      "sequence": 10,
      "label": "Hình vẽ: 3 quả táo đỏ",
      "type": "colored_image",
      "narrativeRole": "Minh họa danh từ số nhiều",
      "region": {
        "x": 600,
        "y": 360,
        "width": 270,
        "height": 190
      },
      "reveal": {
        "direction": "radial_outward",
        "startMs": 7350,
        "durationMs": 1300,
        "protectedRegions": []
      }
    },
    {
      "id": "el-11-label-3apples",
      "sequence": 11,
      "label": "Nhãn: 3 apples",
      "type": "text",
      "narrativeRole": "Ghi chú số lượng 3 quả",
      "region": {
        "x": 580,
        "y": 555,
        "width": 290,
        "height": 90
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 8700,
        "durationMs": 550,
        "protectedRegions": []
      }
    },
    {
      "id": "el-12-one-to-many",
      "sequence": 12,
      "label": "Từ khóa: ONE -> MANY",
      "type": "colored_image",
      "narrativeRole": "Nguyên lý từ 1 sang nhiều",
      "region": {
        "x": 280,
        "y": 650,
        "width": 470,
        "height": 75
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 9300,
        "durationMs": 750,
        "protectedRegions": []
      }
    },

    # DIVIDER MID
    {
      "id": "el-13-divider-mid",
      "sequence": 13,
      "label": "Vách ngăn dọc Zone 2 (giữa Countable và Uncountable)",
      "type": "box",
      "narrativeRole": "Phân chia hai cột so sánh",
      "region": {
        "x": 955,
        "y": 320,
        "width": 10,
        "height": 390
      },
      "reveal": {
        "direction": "top_to_bottom",
        "startMs": 10100,
        "durationMs": 500,
        "protectedRegions": []
      }
    },

    # ZONE 2: UNCOUNTABLE (RIGHT)
    {
      "id": "el-14-hd-uncountable",
      "sequence": 14,
      "label": "Tiêu đề nhóm: UNCOUNTABLE",
      "type": "text",
      "narrativeRole": "Bắt đầu nhóm danh từ không đếm được",
      "region": {
        "x": 1130,
        "y": 320,
        "width": 610,
        "height": 105
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 10650,
        "durationMs": 850,
        "protectedRegions": []
      }
    },
    {
      "id": "el-15-water-glass",
      "sequence": 15,
      "label": "Minh họa: Cốc nước (water)",
      "type": "colored_image",
      "narrativeRole": "Ví dụ chất lỏng không đếm được",
      "region": {
        "x": 1060,
        "y": 360,
        "width": 200,
        "height": 195
      },
      "reveal": {
        "direction": "top_to_bottom",
        "startMs": 11550,
        "durationMs": 950,
        "protectedRegions": []
      }
    },
    {
      "id": "el-16-label-water",
      "sequence": 16,
      "label": "Nhãn: water",
      "type": "text",
      "narrativeRole": "Tên danh từ nước",
      "region": {
        "x": 1060,
        "y": 570,
        "width": 200,
        "height": 145
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 12550,
        "durationMs": 450,
        "protectedRegions": []
      }
    },
    {
      "id": "el-17-rice-bowl",
      "sequence": 17,
      "label": "Minh họa: Bát cơm/gạo (rice)",
      "type": "colored_image",
      "narrativeRole": "Ví dụ dạng hạt nhỏ không đếm được",
      "region": {
        "x": 1330,
        "y": 380,
        "width": 200,
        "height": 175
      },
      "reveal": {
        "direction": "radial_outward",
        "startMs": 13050,
        "durationMs": 950,
        "protectedRegions": []
      }
    },
    {
      "id": "el-18-label-rice",
      "sequence": 18,
      "label": "Nhãn: rice",
      "type": "text",
      "narrativeRole": "Tên danh từ cơm/gạo",
      "region": {
        "x": 1330,
        "y": 570,
        "width": 200,
        "height": 145
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 14050,
        "durationMs": 450,
        "protectedRegions": []
      }
    },
    {
      "id": "el-19-milk-bottle",
      "sequence": 19,
      "label": "Minh họa: Chai sữa (milk)",
      "type": "colored_image",
      "narrativeRole": "Ví dụ chất lỏng sữa",
      "region": {
        "x": 1610,
        "y": 340,
        "width": 170,
        "height": 215
      },
      "reveal": {
        "direction": "top_to_bottom",
        "startMs": 14550,
        "durationMs": 950,
        "protectedRegions": []
      }
    },
    {
      "id": "el-20-label-milk",
      "sequence": 20,
      "label": "Nhãn: milk",
      "type": "text",
      "narrativeRole": "Tên danh từ sữa",
      "region": {
        "x": 1610,
        "y": 570,
        "width": 170,
        "height": 145
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 15550,
        "durationMs": 450,
        "protectedRegions": []
      }
    },

    # DIVIDER ZONE 3
    {
      "id": "el-21-divider-z3",
      "sequence": 21,
      "label": "Đường kẻ ngang phân cách Zone 2 và 3",
      "type": "underline",
      "narrativeRole": "Phân chia khu vực đo lường",
      "region": {
        "x": 0,
        "y": 728,
        "width": 1920,
        "height": 10
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 16050,
        "durationMs": 600,
        "protectedRegions": []
      }
    },

    # ZONE 3: QUANTITY EXPRESSIONS
    {
      "id": "el-22-hd-measure",
      "sequence": 22,
      "label": "Tiêu đề: 3. MEASURE THEM",
      "type": "text",
      "narrativeRole": "Quy tắc dùng đơn vị đo lường cho danh từ không đếm được",
      "region": {
        "x": 40,
        "y": 775,
        "width": 660,
        "height": 85
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 16700,
        "durationMs": 850,
        "protectedRegions": []
      }
    },
    {
      "id": "el-23-unit-water-icon",
      "sequence": 23,
      "label": "Biểu tượng: Ly nước đo lường",
      "type": "colored_image",
      "narrativeRole": "Vật chứa nước",
      "region": {
        "x": 720,
        "y": 750,
        "width": 105,
        "height": 130
      },
      "reveal": {
        "direction": "radial_outward",
        "startMs": 17600,
        "durationMs": 750,
        "protectedRegions": []
      }
    },
    {
      "id": "el-24-unit-water-text",
      "sequence": 24,
      "label": "Cụm từ: a glass of water",
      "type": "text",
      "narrativeRole": "Đơn vị ly nước",
      "region": {
        "x": 820,
        "y": 760,
        "width": 460,
        "height": 105
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 18400,
        "durationMs": 950,
        "protectedRegions": []
      }
    },
    {
      "id": "el-25-unit-rice-icon",
      "sequence": 25,
      "label": "Biểu tượng: Bát cơm đo lường",
      "type": "colored_image",
      "narrativeRole": "Vật chứa cơm/gạo",
      "region": {
        "x": 1290,
        "y": 765,
        "width": 125,
        "height": 110
      },
      "reveal": {
        "direction": "radial_outward",
        "startMs": 19400,
        "durationMs": 750,
        "protectedRegions": []
      }
    },
    {
      "id": "el-26-unit-rice-text",
      "sequence": 26,
      "label": "Cụm từ: a bowl rice",
      "type": "text",
      "narrativeRole": "Đơn vị bát cơm",
      "region": {
        "x": 1410,
        "y": 760,
        "width": 155,
        "height": 105
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 20200,
        "durationMs": 650,
        "protectedRegions": []
      }
    },
    {
      "id": "el-27-unit-milk-icon",
      "sequence": 27,
      "label": "Biểu tượng: Chai sữa đo lường",
      "type": "colored_image",
      "narrativeRole": "Vật chứa sữa",
      "region": {
        "x": 1585,
        "y": 735,
        "width": 80,
        "height": 155
      },
      "reveal": {
        "direction": "top_to_bottom",
        "startMs": 20900,
        "durationMs": 750,
        "protectedRegions": []
      }
    },
    {
      "id": "el-28-unit-milk-text",
      "sequence": 28,
      "label": "Cụm từ: a bottle of milk",
      "type": "text",
      "narrativeRole": "Đơn vị chai sữa",
      "region": {
        "x": 1665,
        "y": 760,
        "width": 195,
        "height": 105
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 21700,
        "durationMs": 750,
        "protectedRegions": []
      }
    },

    # DIVIDER ZONE 4
    {
      "id": "el-29-divider-z4",
      "sequence": 29,
      "label": "Đường kẻ ngang phân cách Zone 3 và 4",
      "type": "underline",
      "narrativeRole": "Phân chia câu ví dụ cuối",
      "region": {
        "x": 0,
        "y": 896,
        "width": 1920,
        "height": 10
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 22500,
        "durationMs": 600,
        "protectedRegions": []
      }
    },

    # ZONE 4: EXAMPLE SENTENCE
    {
      "id": "el-30-sentence",
      "sequence": 30,
      "label": "Câu ví dụ: 4. I need some water.",
      "type": "text",
      "narrativeRole": "Câu ngữ cảnh hoàn chỉnh sử dụng danh từ không đếm được",
      "region": {
        "x": 40,
        "y": 920,
        "width": 1440,
        "height": 115
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 23200,
        "durationMs": 1700,
        "protectedRegions": []
      }
    },
    {
      "id": "el-31-underline-water",
      "sequence": 31,
      "label": "Gạch chân xanh: Dưới từ 'water'",
      "type": "underline",
      "narrativeRole": "Nhấn mạnh danh từ không đếm được duy nhất trong câu",
      "region": {
        "x": 1140,
        "y": 1032,
        "width": 305,
        "height": 26
      },
      "reveal": {
        "direction": "left_to_right",
        "startMs": 25000,
        "durationMs": 700,
        "protectedRegions": []
      }
    }
  ]
}

out_file = Path("assets/whiteboard/test_cases/case_06_countable_uncountable/countable_uncountable.annotation.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(ann, f, indent=2, ensure_ascii=False)
print("Saved annotation to:", out_file)
