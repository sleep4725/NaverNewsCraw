from konlpy.tag import Mecab 

## ===========================
# 작성자: 김준현
# 작성일: 2021-12-08
## ===========================
class Nature:

    def __init__(self):
        self._morpheme = Mecab()
        self._target_tag = ["NNG", "NNP"]

    def get_nng(self, plain_text: str)-> list:
        """

        """
        resp = self._morpheme.pos(plain_text)
        nng_list = list(set([n[0] for n in resp if n[1] in self._target_tag and len(n[0]) >= 2]))
        return nng_list
