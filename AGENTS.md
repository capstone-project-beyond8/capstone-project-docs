# AGENTS.md

## Phạm vi

Các quy tắc này áp dụng cho toàn bộ `capstone-project-docs` và mọi agent làm
việc trong repository này.

## Nguyên tắc làm việc

- Trước khi sửa builder, diagram hoặc thay đổi có thể ảnh hưởng nhiều tài liệu,
  kiểm tra inventory bằng `rg --files`, phạm vi bằng `git status`/`git diff` và
  quan hệ trực tiếp trong source/artifact liên quan.
- Áp dụng SOLID, DRY, KISS và YAGNI; ưu tiên thay đổi nhỏ, source-backed và
  dễ kiểm chứng. Không tạo abstraction hoặc artifact không cần thiết.
- Giữ nguyên các file editable, builder/source và thay đổi không liên quan của
  người dùng. Không thay thế diagram source bằng ảnh phẳng nếu yêu cầu cần
  artifact chỉnh sửa được.

## Documentation-first gate cho commit và PR

Agent MUST hoàn tất việc cập nhật tài liệu trước khi bắt đầu `git commit`,
`git push` hoặc tạo/cập nhật pull request. Không được commit/PR khi tài liệu
đang stale hoặc changelog không phản ánh thay đổi.

Trình tự bắt buộc:

1. Kiểm tra phạm vi thay đổi bằng `git status` và `git diff`; xác định tài liệu
   nguồn và artifact bị ảnh hưởng.
2. Cập nhật tài liệu trước: BRD/PRD/Use Case Spec khi thay đổi requirement,
   scope, actor, rule hoặc flow; cập nhật/regenerate diagram và builder khi
   thay đổi quan hệ hoặc workflow.
3. Cập nhật [`changelog.md`](changelog.md) trong cùng đợt thay đổi, gồm ngày,
   mục đích, file/tài liệu liên quan, validation đã chạy và các reference link.
4. Kiểm tra liên kết trong changelog và các cross-reference không trỏ tới file
   đã xoá/đổi tên; kiểm tra `git diff --check`.
5. Với diagram source-backed, chạy generator phù hợp và validator/render check
   hiện hành trước khi commit; không báo “đã validate” nếu chỉ mới kiểm tra
   syntax.
6. Chỉ sau khi các bước trên hoàn tất mới được stage/commit hoặc mở/cập nhật
   PR. Mô tả commit/PR phải dẫn link tới tài liệu đã cập nhật và nêu validation
   kết quả.

Nếu thay đổi thật sự không làm thay đổi nội dung nghiệp vụ, vẫn phải cập nhật
`changelog.md` để ghi rõ phạm vi và lý do không cần sửa BRD/PRD/Use Case Spec.

## Checklist bắt buộc trước commit/PR

- [ ] `git status`/`git diff` đã được kiểm tra và phạm vi thay đổi rõ ràng.
- [ ] Tài liệu nguồn bị ảnh hưởng đã được cập nhật trước khi commit/PR.
- [ ] Diagram editable và builder liên quan đã đồng bộ, nếu có.
- [ ] `changelog.md` có entry và link tới các tài liệu liên quan.
- [ ] Cross-reference không bị hỏng; `git diff --check` sạch.
- [ ] Validation/render check phù hợp đã chạy và kết quả được ghi trong commit/PR.
- [ ] Không đưa thay đổi không liên quan vào commit/PR.
