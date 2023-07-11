from dataclasses import dataclass, fields


@dataclass
class Gene:
    """
        Class representing gene data
        e.g. C2	brad	gene	247106	248963	.	+	.	ID=gene:Bo2g001300;biotype=protein_coding;gene_id=Bo2g001300;logic_name=brad_maker_pasa

    """
    seqname: str
    source: str
    feature: str
    start: int
    stop: int
    score: float
    strand: str
    frame: str
    id: str
    biotype: str
    description: str
    logic_name: str

    @classmethod
    def create_record(
        cls,
        record: str
    ) -> "Gene":
        fields = record.split("\t")
        # seqname, source,...,frame can be extracted from fields directly.
        ...
        attributes = fields[8]
        attributes_dict = get_dict(attributes)
        id = attributes_dict.get("id")
        alias = attributes_dict.get("alias")
        obj = Gene(
            seqname=seqname,
            source=source,
            feature=feature,
            start=start,
            stop=stop,
            score=score,
            strand=strand,
            frame=frame,
            id=id,
            alias=alias
        )
        return obj

    @classmethod
    def to_csv(
            cls,
            record: Gene
    ) -> str:
        csv_str = ""
        for field in fields(record):
            csv_str += get_value(field)
        return csv_str

