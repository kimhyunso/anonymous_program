"""
logger.py
---------
RunLogger: 익명화를 실행할 때마다 "언제, 무엇을, 어떻게" 치환했는지를
텍스트 로그 파일(anonymize_log.txt)에 추적 가능한 형태로 남김.

주의: 이 로그 파일에는 원본 이름(가명 <-> 실제 값)이 그대로 들어있으므로,
      절대 외부로 공유하지 말고 본인 컴퓨터에만 보관할 것.
"""

import datetime
import uuid
from pathlib import Path


class RunLogger:
    def __init__(self, log_path: str = "anonymize_log.txt"):
        self.log_path = Path(log_path)

    def log_run(self, input_len: int, output: str, mapping: dict) -> str:
        """
        한 번의 익명화 실행 결과를 로그에 추가하고, 추적용 run_id를 반환한다.
        """
        run_id = uuid.uuid4().hex[:8]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        id_count = sum(1 for k in mapping if k.startswith("ID"))
        str_count = sum(1 for k in mapping if k.startswith("'STR"))

        lines = [
            f"=== RUN {timestamp} (ID: {run_id}) ===",
            f"입력 길이: {input_len}자",
            f"치환된 식별자 수: {id_count}",
            f"치환된 문자열 수: {str_count}",
            "[매핑]",
        ]
        for placeholder, original in mapping.items():
            lines.append(f"{placeholder} = {original}")
        lines.append("=== END ===")
        lines.append("")

        with self.log_path.open("a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        return run_id

    def read_all(self) -> str:
        if not self.log_path.exists():
            return ""
        return self.log_path.read_text(encoding="utf-8")

    def find_run(self, run_id: str) -> str:
        """특정 run_id에 해당하는 로그 블록만 찾아서 반환 (추적용)."""
        content = self.read_all()
        blocks = content.split("=== END ===")
        for block in blocks:
            if run_id in block:
                return block.strip() + "\n=== END ==="
        return f"(run id '{run_id}' 를 찾을 수 없습니다)"