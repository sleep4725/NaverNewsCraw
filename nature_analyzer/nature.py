from konlpy.tag import Mecab 

## ===========================
# 작성자: 김준현
# 작성일: 2021-12-08
## ===========================
class Nature:

    def __init__(self, plaintext=""):
        """ plaintext : 원문 
        """
        self._morpheme = Mecab()
        self._target_tag = ["NNG", "NNP"]
        # =======================================================
        self.plaintext = str(plaintext).strip() # 양쪽 공백 제거
        self.mecab_result = self._morpheme.pos(plaintext)
        print(self.mecab_result)
        self.indx = 0
        
        self.compound_noun = "" # 복합명사
        self.compound_noun_list = [] # 복합명사 리스트

    def ret_mecab_result(self)-> list:
        """
        """
        if self.plaintext:
            resp = self._morpheme.pos(self.plaintext)
            return resp 
        else:
            return [] 
    
    def plaintext_index_move(self, plaintext_index):
        """
        """
        flag = True
        while True:
            
            if self.plaintext[plaintext_index] != " ":
                break
            else:
                plaintext_index += 1
                flag = False

        return plaintext_index, flag

    def nng(self, mecab_index, word_length, plaintext_index)-> int:
        """
        aa bbcc dd eeff
        :param: mecab_index
        :param: word_length
        :return:
        """
        while True:

            if self.mecab_result[mecab_index+1][1] == "NNG": 
                
                next_word = self.plaintext[plaintext_index + word_length] 

                if next_word == self.mecab_result[mecab_index+1][0][0]:
                    #print(f"p: {next_word} | {self.mecab_result[mecab_index+1][0][0]}")
                    self.compound_noun += self.mecab_result[mecab_index+1][0] 
                    
                    plaintext_index += len(self.mecab_result[mecab_index][0])
                    mecab_index += 1 # 단어 이동
                    #plaintext_index += len(self.mecab_result[mecab_index][0]) 
                    word_length = plaintext_index 

                    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    plaintext_index, flag = self.plaintext_index_move(plaintext_index)
                    if not flag:
                        self.compound_noun_list.append(self.compound_noun)
                        self.compound_noun = "" # 초기화 
                        break
                    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                else:
                    plaintext_index += len(self.mecab_result[mecab_index][0])
                    plaintext_index,_ = self.plaintext_index_move(plaintext_index)
                    mecab_index += 1
                    break

            else:
                plaintext_index += len(self.mecab_result[mecab_index][0])
                plaintext_index,_ = self.plaintext_index_move(plaintext_index)
                mecab_index += 1
                break

        return mecab_index , plaintext_index 

    def get_nng(self)-> list:
        """
        :param:
        :return:
        """
        mecab_index = 0 # 단어의 위치
        word_length = 0 # 단어의 길이 
        plaintext_index = 0 # 원문의 인덱스 위치 

        while mecab_index < len(self.mecab_result)-1:
            
            print(mecab_index, plaintext_index, self.plaintext[plaintext_index])
            
            # 내년 0 0 2
            if self.mecab_result[mecab_index][1] == "NNG":
                ## 일반 명사라면 
                self.compound_noun += self.mecab_result[mecab_index][0] 
               
                #plaintext_index += len(self.mecab_result[mecab_index][0])

                # 그 다음 단어 확인 
                plaintext_index, flag = self.plaintext_index_move(plaintext_index)
                
                if flag: 
                    # ====================================
                    # 그 다음 단어를 반드시 확인해야 한다.
                    # ====================================
                    print("check")
                    mecab_index, plaintext_index = self.nng(mecab_index, len(self.mecab_result[mecab_index][0]), plaintext_index)
                else:
                    #self.compound_noun_list.append(self.mecab_result[mecab_index][0])
                    #self.compound_noun = ""
                    #plaintext_index,_ = self.plaintext_index_move(plaintext_index)
                    mecab_index += 1
                    #plaintext_index += len(self.mecab_result[mecab_index][0])

                self.compound_noun_list.append(self.compound_noun) # 복합명사를 리스트에 적재  
                self.compound_noun = "" # 복합명사 문자열 초기화 
            else:
                # word != NNG
                plaintext_index += len(self.mecab_result[mecab_index][0]) # 단어 이동
                plaintext_index,_ = self.plaintext_index_move(plaintext_index)
                mecab_index += 1
                self.compound_noun = ""
    
    def result_compound_list(self):
        """
        """
        result_list = [ w for w in list(set(self.compound_noun_list)) if len(w) >= 2 ]
        print(result_list)

if __name__ == "__main__":
    #p = "미국 시사주간지 타임은 13일(현지시간) 테슬라와 스페이스X를 이끌고 있는 일론 머스크를 2021년 올해의 인물로 선정했다고 발표했다."
    p = "내년 대선을 3개월여 앞두고 이재명 더불어민주당 대선후보와 윤석열 국민의힘 대선후보 측의 ‘청년 행보’가 활발하다."
    # ['시사', '주간지타임', '', '타임', '현지시간', '스페이스', '일', '머스크', '올해', '인물', '선정', '발표']
    print(p)
    o = Nature(plaintext=p)
    o.get_nng()
    o.result_compound_list()
