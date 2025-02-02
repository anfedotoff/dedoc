from typing import Optional, Dict

from dedoc.common.exceptions.structure_extractor_exception import StructureExtractorException
from dedoc.data_structures.parsed_document import ParsedDocument
from dedoc.data_structures.unstructured_document import UnstructuredDocument
from dedoc.structure_constructors.abstract_structure_constructor import \
    AbstractStructureConstructor
from dedoc.structure_constructors.table_patcher import TablePatcher


class StructureConstructorComposition(AbstractStructureConstructor):

    def __init__(self,
                 extractors: Dict[str, AbstractStructureConstructor],
                 default_extractor: AbstractStructureConstructor) -> None:
        self.extractors = extractors
        self.default_extractor = default_extractor
        self.table_patcher = TablePatcher()

    def structure_document(self,
                           document: UnstructuredDocument,
                           version: str,
                           structure_type: Optional[str] = None,
                           parameters: dict = None) -> ParsedDocument:
        if parameters is None:
            parameters = {}
        if parameters.get("insert_table", "False").lower() == "true":
            document = self.table_patcher.insert_table(document=document)

        if structure_type in self.extractors:
            return self.extractors[structure_type].structure_document(document, structure_type)

        if structure_type is None or structure_type == "":
            return self.default_extractor.structure_document(document, version, structure_type)

        raise StructureExtractorException("Bad structure type {}, available structure types is: {}".format(
            structure_type, " ".join(self.extractors.keys())
        ))
