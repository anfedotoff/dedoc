from collections import OrderedDict
from typing import Optional, List
from flask_restx import fields, Api, Model

from src.data_structures.serializable import Serializable
from src.data_structures.cell_property import CellProperty


class TableMetadata(Serializable):

    def __init__(self, page_id: Optional[int], uid: str = "", is_inserted: bool = False,
                 cell_properties: Optional[List[List[CellProperty]]] = None) -> None:
        """
        Holds the information about the table location in the document and information about cell properties
        :param page_id: number of page where table starts
        :uid: unique id of table
        :was_inserted: if table was already inserted into paragraphs list
        :cell_properties: content different property of each cell
        """
        self.page_id = page_id
        self.uid = uid
        self.is_inserted = is_inserted
        self.cell_properties = cell_properties

    def to_dict(self, old_version: bool) -> dict:
        res = OrderedDict()
        res["uid"] = self.uid
        res["page_id"] = self.page_id
        res["is_inserted"] = self.is_inserted
        res["cell_properties"] = [[cell_prop.to_dict(old_version) for cell_prop in row_prop]
                                  for row_prop in self.cell_properties] if self.cell_properties else None
        return res

    @staticmethod
    def get_api_dict(api: Api) -> Model:
        return api.model('TableMetadata', {
            'page_id': fields.Integer(readonly=False, description='table start page number'),
            'uid': fields.String(description="table unique id"),
            'is_inserted': fields.Boolean(description="was the table inserted into document body"),
            'cell_properties': fields.List(fields.List(fields.Nested(CellProperty.get_api_dict(api),
                                                                     description="cell properties, colspan, rowspan, "
                                                                                 "etc",
                                                                     allow_null=True,
                                                                     skip_none=True)))
        })