# BƯỚC 2 — VOICE-OVER SCRIPT & AUDIO MASTER CLOCK
## Dự án: ARTICLES — Bài 1: A / AN
> **Trạng thái:** Bản lời thoại và SRT dưới đây là bản nháp căn theo Scene Matrix và prompt đã duyệt. Chưa thể xác nhận đã duyệt ảnh thực tế hoặc đo âm thanh đến mili-giây: trong cuộc trò chuyện hiện chỉ có hai file Markdown của Bước 0/Bước 1, chưa có 9 ảnh đầu ra và chưa có file audio. Cần đối chiếu lại script với ảnh thật trước khi khóa script, rồi đo timing sau khi render TTS.
## 1. Thông số đã giữ nguyên
- Đối tượng: người Việt mới học tiếng Anh hoàn toàn.
- Thời lượng đích: 7 phút 30 giây (450 giây), nằm trong phạm vi 6–8 phút.
- 9 scene theo ma trận đã duyệt.
- Giọng đọc phần giải thích: nam miền Bắc, điềm tĩnh, truyền cảm.
- Từ và câu tiếng Anh: American English (Mỹ), phát âm đúng, không Việt hóa.
- Hình ảnh: 2D Whiteboard Animation, nền trắng, không nhân vật giáo viên.
- Khoảng nghỉ mục tiêu: 0,5 giây giữa câu thông thường; phần suy nghĩ trong quiz chính xác 3 giây; giữ khung cuối scene ít nhất 2 giây.
## 2. Lưu ý khi tổng hợp giọng đọc
1. Nếu dùng một TTS đa ngôn ngữ, kiểm tra riêng cách đọc các đoạn tiếng Anh. Nếu tiếng Anh bị Việt hóa, hãy render các từ/cụm tiếng Anh bằng giọng en-US rồi ghép vào narration tiếng Việt, hoặc dùng một engine đa ngôn ngữ có khả năng code-switching tốt.
2. Voice-over phải bám vào đúng element đang xuất hiện: không đọc nhãn trước khi nó được vẽ; không tiết lộ đáp án trước khi hết 3 giây suy nghĩ.
3. Với từng scene, giữ tối thiểu 2 giây không lời ở cuối để khán giả quan sát. Scene 09 hiện có 5 giây cuối làm nhịp kết.
4. Các mốc ở tài liệu và file SRT là **mốc dựng nháp**, không phải thời lượng đã đo từ TTS. Sau khi tạo audio thật, đo duration và waveform, chia lại cue SRT theo thời điểm âm thanh thực tế. Không ép tốc độ TTS để khớp với SRT nháp nếu làm giọng thiếu tự nhiên.
## 3. Voice Direction đề xuất
- Vietnamese narration: giọng nam miền Bắc; điềm tĩnh, rõ phụ âm cuối, truyền cảm vừa phải; tốc độ hướng dẫn cho người mới, không đọc dồn dập.
- English spans: American English, phát âm tự nhiên và nhất quán. Các cặp cần kiểm tra kỹ: `a book`, `an apple`, `an hour`, `an honest man`, `a university`, `a European country`.
- Nhấn bằng giọng: `A`, `AN`, `first sound`, `not letter`; không tăng âm lượng quá mạnh.
- TTS mix: âm lượng narration ổn định; không có nhạc hoặc hiệu ứng lấn tiếng ở giai đoạn kiểm tra đồng bộ.
## 4. Lời thoại theo scene và liên kết hình ảnh
### Scene 01 — 00:00:00.000 đến 00:00:45.000 (45 giây)
| Mốc nháp | Voice-over | Element/hành động hình ảnh cần đồng bộ |
|---|---|---|
| 00:00.0–00:06.5 | Trong tiếng Anh, những từ ngắn đứng trước danh từ được gọi là mạo từ, hay Articles. | Scene 01: title ARTICLES; overall concept |
| 00:07.0–00:15.0 | Có ba nhóm cần biết: A và AN, THE, và trường hợp không dùng mạo từ, gọi là Zero Article. | Scene 01: three cards A / AN, THE, ZERO ARTICLE |
| 00:15.5–00:25.5 | Mỗi nhóm có cách dùng riêng. Hôm nay, chúng ta chỉ tập trung vào A và AN. | Scene 01: highlight TODAY: A / AN |
| 00:26.0–00:35.0 | Bạn sẽ học cách nhận biết nguyên âm, phụ âm và chọn mạo từ theo âm đầu của từ. | Scene 01: bottom emphasis; prepare transition to Scene 02 |
| 00:35.5–00:43.0 | Sau đó, hãy quan sát ví dụ và tự chọn đáp án trong năm câu luyện tập. | Scene 01: intro promises examples and five practice questions |

**Cuối scene:** giữ hình tĩnh khoảng 2 giây sau câu cuối (tối thiểu 2 giây). Kiểm tra timing theo audio thực tế trước khi khóa.
### Scene 02 — 00:00:45.000 đến 00:01:35.000 (50 giây)
| Mốc nháp | Voice-over | Element/hành động hình ảnh cần đồng bộ |
|---|---|---|
| 00:45.0–00:50.0 | Trước tiên, hãy nhìn vào bảng chữ cái tiếng Anh. | Scene 02: title VOWELS & CONSONANTS |
| 00:50.5–00:59.5 | Năm chữ cái thường được gọi là nguyên âm là A, E, I, O, U. | Scene 02: blue A E I O U group |
| 01:00.0–01:07.0 | Các chữ cái còn lại thường được xếp vào nhóm phụ âm cơ bản. | Scene 02: consonant-letter group |
| 01:07.5–01:15.0 | Riêng chữ Y đôi khi đại diện cho âm nguyên âm trong một số từ. | Scene 02: separate Y note |
| 01:15.5–01:24.0 | Nhưng chữ cái và âm thanh không phải lúc nào cũng cho ta cùng một câu trả lời. | Scene 02: hold on the two letter groups; introduce letter-versus-sound idea |
| 01:24.5–01:33.0 | Khi chọn A hay AN, điều quan trọng là âm đầu tiên ta nghe được. | Scene 02: highlight the sound concept before transition |

**Cuối scene:** giữ hình tĩnh khoảng 2 giây sau câu cuối (tối thiểu 2 giây). Kiểm tra timing theo audio thực tế trước khi khóa.
### Scene 03 — 00:01:35.000 đến 00:02:25.000 (50 giây)
| Mốc nháp | Voice-over | Element/hành động hình ảnh cần đồng bộ |
|---|---|---|
| 01:35.0–01:42.0 | A và AN được gọi là mạo từ không xác định. | Scene 03: title WHAT ARE A AND AN? |
| 01:42.5–01:52.0 | Ở mức cơ bản, chúng thường đứng trước danh từ đếm được số ít khi nói đến một người hoặc vật chưa xác định cụ thể. | Scene 03: ONE + COUNTABLE NOUN concept |
| 01:52.5–02:00.0 | Ví dụ, một cuốn sách: a book. | Scene 03: book icon and label a book; pronounce English phrase in American English |
| 02:00.5–02:08.0 | Một quả táo: an apple. | Scene 03: apple icon and label an apple; pronounce English phrase in American English |
| 02:08.5–02:17.0 | Ta không dùng A hoặc AN trực tiếp trước danh từ số nhiều như books, hoặc danh từ không đếm được như water. | Scene 03: concept reminder; if those comparison words are not on the generated image, do not imply they are visible |
| 02:17.5–02:23.0 | Bài học này tập trung vào danh từ đếm được số ít. | Scene 03: bottom reminder ONE + COUNTABLE NOUN |

**Cuối scene:** giữ hình tĩnh khoảng 2 giây sau câu cuối (tối thiểu 2 giây). Kiểm tra timing theo audio thực tế trước khi khóa.
### Scene 04 — 00:02:25.000 đến 00:03:15.000 (50 giây)
| Mốc nháp | Voice-over | Element/hành động hình ảnh cần đồng bộ |
|---|---|---|
| 02:25.0–02:31.0 | Bây giờ, đến quy tắc quan trọng nhất. | Scene 04: title A OR AN? and FIRST SOUND |
| 02:31.5–02:40.0 | Dùng A trước từ bắt đầu bằng âm phụ âm. | Scene 04: CONSONANT SOUND branch and A label |
| 02:40.5–02:49.0 | Dùng AN trước từ bắt đầu bằng âm nguyên âm. | Scene 04: VOWEL SOUND branch and AN label |
| 02:49.5–02:57.0 | Hãy nhìn ví dụ a book. Từ book bắt đầu bằng âm phụ âm, nên ta dùng A. | Scene 04: book icon and a book label |
| 02:57.5–03:05.0 | Với an apple, apple bắt đầu bằng âm nguyên âm, nên ta dùng AN. | Scene 04: apple icon and an apple label |
| 03:05.5–03:13.0 | Đây là điểm mấu chốt: nghe âm đầu, đừng chỉ nhìn chữ cái đầu tiên. | Scene 04: bottom reminder SOUND, NOT LETTER |

**Cuối scene:** giữ hình tĩnh khoảng 2 giây sau câu cuối (tối thiểu 2 giây). Kiểm tra timing theo audio thực tế trước khi khóa.
### Scene 05 — 00:03:15.000 đến 00:04:05.000 (50 giây)
| Mốc nháp | Voice-over | Element/hành động hình ảnh cần đồng bộ |
|---|---|---|
| 03:15.0–03:21.0 | Bây giờ, hãy thử với những từ quen thuộc. | Scene 05: title COMMON EXAMPLES |
| 03:21.5–03:29.0 | A book, a cat, a car. Các từ này đều bắt đầu bằng âm phụ âm. | Scene 05: three icons and labels in A group; pronounce English examples in American English |
| 03:29.5–03:38.0 | An apple, an egg, an umbrella. Các từ này bắt đầu bằng âm nguyên âm. | Scene 05: three icons and labels in AN group; pronounce English examples in American English |
| 03:38.5–03:47.0 | Mạo từ đứng ngay trước danh từ hoặc cụm danh từ. Hãy nghe từ được nói ngay sau A hoặc AN. | Scene 05: compare left and right groups |
| 03:47.5–03:56.0 | Đừng chỉ học thuộc hình dáng chữ cái. Hãy kết hợp từ với cách phát âm của nó. | Scene 05: visual contrast between the A and AN groups |
| 03:56.5–04:03.0 | Tiếp theo, chúng ta sẽ gặp những từ dễ gây nhầm lẫn hơn. | Scene 05: transition toward Scene 06 |

**Cuối scene:** giữ hình tĩnh khoảng 2 giây sau câu cuối (tối thiểu 2 giây). Kiểm tra timing theo audio thực tế trước khi khóa.
### Scene 06 — 00:04:05.000 đến 00:05:00.000 (55 giây)
| Mốc nháp | Voice-over | Element/hành động hình ảnh cần đồng bộ |
|---|---|---|
| 04:05.0–04:11.0 | Bây giờ, hãy xem bốn trường hợp dễ gây nhầm lẫn. | Scene 06: title SPECIAL CASES and FIRST SOUND |
| 04:11.5–04:20.0 | Đầu tiên, an hour. Chữ H ở đầu hour không được phát âm, nên âm đầu tiên là âm nguyên âm. | Scene 06: clock, an hour, H IS SILENT |
| 04:20.5–04:29.0 | Tương tự, an honest man. Chữ H trong honest cũng không được phát âm. | Scene 06: man illustration, an honest man, H IS SILENT |
| 04:29.5–04:38.0 | Ngược lại, a university. Dù viết bằng chữ U, từ bắt đầu bằng âm giống chữ Y trong yes. | Scene 06: university illustration and STARTS WITH Y SOUND |
| 04:38.5–04:48.0 | Và a European country cũng bắt đầu bằng âm Y đó, nên ta dùng A chứ không phải AN. | Scene 06: Europe/globe illustration and STARTS WITH Y SOUND |
| 04:48.5–04:57.0 | Hãy nhớ: lựa chọn phụ thuộc vào âm đầu tiên khi phát âm từ, không chỉ vào chữ cái viết đầu tiên. | Scene 06: all four cases; reinforce first-sound principle |

**Cuối scene:** giữ hình tĩnh khoảng 3 giây sau câu cuối (tối thiểu 2 giây). Kiểm tra timing theo audio thực tế trước khi khóa.
### Scene 07 — 00:05:00.000 đến 00:05:50.000 (50 giây)
| Mốc nháp | Voice-over | Element/hành động hình ảnh cần đồng bộ |
|---|---|---|
| 05:00.0–05:07.0 | Để chọn đúng, bạn có thể làm theo ba bước đơn giản. | Scene 07: title HOW TO CHOOSE |
| 05:07.5–05:14.0 | Bước một: nhìn từ hoặc hình ảnh và xác định từ cần điền mạo từ. | Scene 07: LOOK step and eye icon |
| 05:14.5–05:21.0 | Bước hai: đọc từ đó hoặc nhớ cách phát âm chính xác của nó. | Scene 07: SAY step and mouth icon |
| 05:21.5–05:30.0 | Bước ba: nghe âm đầu. Âm phụ âm thì chọn A; âm nguyên âm thì chọn AN. | Scene 07: LISTEN, FIRST SOUND, and two answer branches |
| 05:30.5–05:38.0 | Ví dụ, a book và an apple. Hãy đọc cả cụm để nghe âm đầu của từ đứng sau mạo từ. | Scene 07: example book and apple |
| 05:38.5–05:47.0 | Nếu chưa biết cách đọc một từ, hãy nghe mẫu phát âm trước khi chọn. Đừng đoán chỉ theo mặt chữ. | Scene 07: SOUND, NOT LETTER reminder |

**Cuối scene:** giữ hình tĩnh khoảng 3 giây sau câu cuối (tối thiểu 2 giây). Kiểm tra timing theo audio thực tế trước khi khóa.
### Scene 08 — 00:05:50.000 đến 00:06:40.000 (50 giây)
| Mốc nháp | Voice-over | Element/hành động hình ảnh cần đồng bộ |
|---|---|---|
| 05:50.0–05:54.0 | Đến lượt bạn. Hãy chọn A hay AN. | Scene 08: quiz title CHOOSE A OR AN |
| 05:54.5–05:58.0 | Câu một: ___ dog. Bạn có ba giây để suy nghĩ. | Scene 08 Q1: dog, options A and AN; then 3-second silence |
| 06:01.0–06:06.0 | Đáp án là a dog, vì dog bắt đầu bằng âm phụ âm. | Scene 08 Q1: draw/check A after thinking pause |
| 06:06.5–06:10.5 | Câu hai: ___ orange. A hay AN? Hãy suy nghĩ trong ba giây. | Scene 08 Q2: orange, options A and AN; then 3-second silence |
| 06:13.5–06:19.0 | Đáp án là an orange, vì orange bắt đầu bằng âm nguyên âm. | Scene 08 Q2: draw/check AN after thinking pause |
| 06:19.5–06:23.5 | Câu ba: ___ egg. Hãy chọn trong ba giây. | Scene 08 Q3: egg, options A and AN; then 3-second silence |
| 06:26.5–06:32.0 | Đáp án là an egg, vì egg bắt đầu bằng âm nguyên âm. | Scene 08 Q3: draw/check AN after thinking pause |
| 06:32.5–06:38.0 | Hãy nhớ quy tắc và luôn chú ý đến âm đầu tiên của từ. | Scene 08: bottom THINK FIRST reminder and transition |

**Cuối scene:** giữ hình tĩnh khoảng 2 giây sau câu cuối (tối thiểu 2 giây). Kiểm tra timing theo audio thực tế trước khi khóa.
### Scene 09 — 00:06:40.000 đến 00:07:30.000 (50 giây)
| Mốc nháp | Voice-over | Element/hành động hình ảnh cần đồng bộ |
|---|---|---|
| 06:40.0–06:44.0 | Hai câu cuối là những thử thách đặc biệt. | Scene 09: FINAL CHALLENGE |
| 06:44.5–06:48.5 | Câu bốn: ___ hour. A hay AN? Bạn có ba giây. | Scene 09 Q4: hour and choices; then 3-second silence |
| 06:51.5–06:57.0 | Đáp án là an hour, vì chữ H đầu không được phát âm. | Scene 09 Q4: draw/check AN after thinking pause |
| 06:57.5–07:01.5 | Câu năm: ___ university. A hay AN? Bạn có ba giây. | Scene 09 Q5: university and choices; then 3-second silence |
| 07:04.5–07:10.0 | Đáp án là a university, vì từ bắt đầu bằng âm Y giống trong yes. | Scene 09 Q5: draw/check A after thinking pause |
| 07:10.5–07:18.5 | Hãy ghi nhớ: A đứng trước âm phụ âm; AN đứng trước âm nguyên âm. Nghe âm đầu, đừng chỉ nhìn chữ cái. | Scene 09: final two-rule summary |
| 07:19.0–07:25.0 | Bài tiếp theo, chúng ta sẽ học mạo từ THE. | Scene 09: close lesson and point toward next topic THE |

**Cuối scene:** giữ hình tĩnh khoảng 5 giây sau câu cuối (tối thiểu 2 giây). Kiểm tra timing theo audio thực tế trước khi khóa.
## 5. Quy tắc subtitle và timing
- Một cue SRT tương ứng một câu hoặc một câu hỏi/đáp án ngắn.
- Không tạo phụ đề trong 3 giây im lặng để người học suy nghĩ; tuy nhiên hình câu hỏi vẫn giữ trên màn hình.
- 0,5 giây nghỉ giữa các câu thông thường được để trống, không cần cue phụ đề.
- File `input_DRAFT.srt` chỉ là bản dựng nháp theo mốc scene 7:30. Khi có `narration.m4a`, cần cập nhật timecode theo audio thực tế đến mili-giây.
## 6. Câu hỏi luyện tập — đáp án kiểm tra nội dung
| Câu | Prompt hiển thị | Đáp án | Lý do |
|---|---|---|---|
| 1 | ___ dog | A — a dog | Âm đầu /d/ là âm phụ âm. |
| 2 | ___ orange | AN — an orange | Âm đầu của orange là âm nguyên âm. |
| 3 | ___ egg | AN — an egg | Âm đầu của egg là âm nguyên âm. |
| 4 | ___ hour | AN — an hour | H đầu từ không được phát âm. |
| 5 | ___ university | A — a university | University bắt đầu bằng âm /j/, giống âm đầu của yes. |

## 7. Kiểm tra trước khi khóa Bước 2
- [ ] Đã đối chiếu tất cả 9 ảnh thực tế; nếu text hoặc element không có trong ảnh thì sửa script/ảnh, không giả định ảnh giống prompt.
- [ ] Đã tạo và nghe duyệt `narration.m4a`; phát âm tiếng Anh theo American English.
- [ ] Đã kiểm tra riêng các ví dụ `an hour`, `an honest man`, `a university`, `a European country`.
- [ ] Đã đo thời lượng thực tế và cập nhật SRT theo audio, không dùng timing nháp làm timing cuối.
- [ ] Mỗi câu hỏi có đúng 3 giây suy nghĩ trước khi đáp án xuất hiện trong hình và lời thoại.
- [ ] Mỗi scene có ít nhất 2 giây tĩnh ở cuối; tổng duration video được tính lại từ audio thật.
