from collections import defaultdict
from typing import List

from src.readers.scanned_reader.data_classes.bbox import BBox
from src.readers.scanned_reader.pdfscanned_reader.ocr_page.ocr_line import OcrLine
from src.readers.scanned_reader.pdfscanned_reader.ocr_page.ocr_tuple import OcrElement


class OcrParagraph:

    level = 3

    def __init__(self, order: int, bbox: BBox, lines: List[OcrLine]) -> None:
        super().__init__()
        self.order = order
        self.bbox = bbox
        self.lines = sorted(lines, key=lambda line: line.order)

    @property
    def text(self) -> str:
        return "\n".join(line.text for line in self.lines)

    @staticmethod
    def from_list(paragraph: List[OcrElement], ocr_conf_thr: float) -> "OcrParagraph":
        line2element = defaultdict(list)
        head = None
        for element in paragraph:
            if element.level > OcrParagraph.level:
                line2element[element.line_num].append(element)
            else:
                head = element

        lines = [OcrLine.from_list(line=line2element[key], ocr_conf_thr=ocr_conf_thr) for key in sorted(line2element.keys())]
        return OcrParagraph(order=head.paragraph_num, lines=lines, bbox=head.bbox)