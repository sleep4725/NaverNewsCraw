from konlpy.tag import Mecab 

## ===========================
# 작성자: 김준현
# 작성일: 2021-12-08
## ===========================
class Nature:

    def __init__(self, plaintext=""):
        """ 
        :param: plaintext : 원문 
        """
        self._morpheme = Mecab()
        self._target_tag = ["NNG", "NNP"]
        # =======================================================
        self.plaintext = str(plaintext).strip() # 양쪽 공백 제거
        self.mecab_result = self._morpheme.pos(plaintext)
        #print(self.mecab_result)
        self.indx = 0
        
        self.compound_noun = "" # 복합명사
        self.compound_noun_list = [] # 복합명사 리스트

    def ret_mecab_result(self)-> list:
        """
        :param:
        :return:
        """
        if self.plaintext:
            resp = self._morpheme.pos(self.plaintext)
            return resp 
        else:
            return [] 
    
    def plaintext_index_move(self, plaintext_index):
        """
        :param: plaintext_index
        :return:
        """
        flag = True
        while plaintext_index < len(self.plaintext):
            
            if self.plaintext[plaintext_index] != " ":
                break
            else:
                plaintext_index += 1
                flag = False

        return plaintext_index, flag
    
    def nnp(self, mecab_index, word_length, plaintext_index)-> tuple:
        """
        :param: mecab_index
        :param: word_length
        :param: plaintext_index
        :return:
        """
        while True:

            if self.mecab_result[mecab_index+1][1] == "NNP":

                next_word = self.plaintext[plaintext_index + word_length]

                if next_word == self.mecab_result[mecab_index+1][0][0]:
                    self.compound_noun += self.mecab_result[mecab_index+1][0]

                    plaintext_index += len(self.mecab_result[mecab_index][0])
                    mecab_index += 1 # 단어 이동 
                    word_length = len(self.mecab_result[mecab_index][0])
                    
                    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    plaintext_index, flag = self.plaintext_index_move(plaintext_index)
                    if not flag:
                        self.compound_noun_list.append(self.compound_noun)
                        self.compound_noun = "" # 초기화
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


    def nng(self, mecab_index, word_length, plaintext_index)-> tuple: 
        """
        (XPN)+NNG+(XSN) :  비과학적(비/XPN+과학/NNG+적/XSN),   신제품(신/XPN+제품/NNG), 책들(책/NNG+들/XSN )
        (XPN)+NNG+NNG+(XSN)
        (XPN)+NNG+NNB+(XSN) : 무의식간(무/XPN+의식/NNG+간/NNB)
        (XPN)+XR+(XSN)
        :param: mecab_index
        :param: word_length
        :return:
        """
        merge_word = False 
        check_xr_bool = False 

        while mecab_index+1 < len(self.mecab_result):
            ##
            #print(self.mecab_result[mecab_index+1][1])

            if self.mecab_result[mecab_index+1][1] in ["NNG", "NNP"]: 
                
                next_word = self.plaintext[plaintext_index + word_length] 
                #print(f"p: {next_word} | {self.mecab_result[mecab_index+1][0]}")

                if next_word == self.mecab_result[mecab_index+1][0][0]:
                    merge_word = True
                    #print(f"p: {next_word} | {self.mecab_result[mecab_index+1][0]}")
                    self.compound_noun += self.mecab_result[mecab_index+1][0] 
                    
                    plaintext_index += len(self.mecab_result[mecab_index][0])
                    mecab_index += 1 # 단어 이동
                    #plaintext_index += len(self.mecab_result[mecab_index][0]) 
                    #word_length = plaintext_index 
                    word_length = len(self.mecab_result[mecab_index][0]) 

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

            elif self.mecab_result[mecab_index+1][1] in ["NNB","NNBC"] :
                # -> NNB(의존명사)
                next_word = self.plaintext[plaintext_index + word_length]
                if next_word == self.mecab_result[mecab_index+1][0][0]:
                    merge_word = True
                    self.compound_noun += self.mecab_result[mecab_index+1][0]

                    plaintext_index += len(self.mecab_result[mecab_index][0])
                    mecab_index += 1 # 단어 이동
                    word_length = len(self.mecab_result[mecab_index][0])

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
            #  
            elif self.mecab_result[mecab_index+1][1] == "XSN":
                # -> XSN(명사파생 접미사)
                next_word = self.plaintext[plaintext_index + word_length]

                if next_word == self.mecab_result[mecab_index+1][0][0]:
                    merge_word = True
                    self.compound_noun += self.mecab_result[mecab_index+1][0]

                    plaintext_index += len(self.mecab_result[mecab_index][0])
                    mecab_index += 1 # 단어 이동
                    word_length = len(self.mecab_result[mecab_index][0])

                    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    plaintext_index,_ = self.plaintext_index_move(plaintext_index) 
                    break
                    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                else:
                    plaintext_index += len(self.mecab_result[mecab_index][0])
                    plaintext_index,_ = self.plaintext_index_move(plaintext_index)
                    mecab_index += 1
                    break 
            #
            else:
                plaintext_index += len(self.mecab_result[mecab_index][0])
                plaintext_index,_ = self.plaintext_index_move(plaintext_index)
                mecab_index += 1
                break

        return mecab_index, plaintext_index, merge_word 

    def get_nng(self)-> list:
        """
        :param:
        :return:
        """
        mecab_index = 0 # 단어의 위치
        word_length = 0 # 단어의 길이 
        plaintext_index = 0 # 원문의 인덱스 위치 

        while mecab_index+1 < len(self.mecab_result):
            
            #print("check : {}   mecab_index : {}".format(self.mecab_result[mecab_index][1], mecab_index))

            if self.mecab_result[mecab_index][1] in ["NNG", "NNP"]:
                print("nng -> {}".format(self.mecab_result[mecab_index][0]))
                # ===================
                # 일반명사 
                # ===================
                self.compound_noun += self.mecab_result[mecab_index][0] 
               
                #plaintext_index += len(self.mecab_result[mecab_index][0])

                # 그 다음 단어 확인 
                plaintext_index, flag = self.plaintext_index_move(plaintext_index)
                
                if flag: 
                    # ====================================
                    # 그 다음 단어를 반드시 확인해야 한다.
                    # ====================================
                    mecab_index, plaintext_index, merge_word_bool = self.nng(mecab_index, len(self.mecab_result[mecab_index][0]), plaintext_index)
                else:
                    #self.compound_noun_list.append(self.mecab_result[mecab_index][0])
                    #self.compound_noun = ""
                    #plaintext_index,_ = self.plaintext_index_move(plaintext_index)
                    mecab_index += 1
                    #plaintext_index += len(self.mecab_result[mecab_index][0])

                self.compound_noun_list.append(self.compound_noun) # 복합명사를 리스트에 적재  
                self.compound_noun = "" # 복합명사 문자열 초기화 
            
            elif self.mecab_result[mecab_index][1] in ["XPN", "MM"]:
                # ======================
                # 체언 접두사
                # ======================
                self.compound_noun += self.mecab_result[mecab_index][0]
                merge_word_bool = False

                # 그 다음 단어 확인
                plaintext_index, flag = self.plaintext_index_move(plaintext_index)
                if flag:
                    mecab_index, plaintext_index, merge_word_bool = self.nng(mecab_index, len(self.mecab_result[mecab_index][0]), plaintext_index)
                else:
                    mecab_index += 1

                if merge_word_bool:
                    self.compound_noun_list.append(self.compound_noun)
                    self.compound_noun = ""
            
                """
                elif self.mecab_result[mecab_index][1] == "NNP":
                    # =======================
                    # 고유 명사 
                    # =======================
                    self.compound_noun += self.mecab_result[mecab_index][0] 
                    
                    # 그 다음 단어 확인 
                    plaintext_index, flag = self.plaintext_index_move(plaintext_index)
                    if flag:
                        #print("nnp check")
                        mecab_index, plaintext_index, merge_word_bool = self.nng(mecab_index, len(self.mecab_result[mecab_index][0]), plaintext_index) 
                    else:
                        mecab_index += 1
                    
                    self.compound_noun_list.append(self.compound_noun) # 복합명사를 리스트에 적재
                    self.compound_noun = "" # 복합명사 문자열 초기화
                """
            elif self.mecab_result[mecab_index][1] == "VV+ETN":
                # 
                #
                # 
                self.compound_noun += self.mecab_result[mecab_index][0]
                self.compound_noun_list.append(self.compound_noun)
                self.compound_noun = "" # 복합명사 문자열 초기화
                plaintext_index, _ = self.plaintext_index_move(plaintext_index) 
                mecab_index += 1

            elif self.mecab_result[mecab_index][1] == "VA+ETN":
                #
                #
                #
                self.compound_noun += self.mecab_result[mecab_index][0]
                self.compound_noun_list.append(self.compound_noun)
                self.compound_noun = "" # 복합명사 문자열 초기화
                plaintext_index, _ = self.plaintext_index_move(plaintext_index)
                mecab_index += 1

            else:
                # word != NNG
                plaintext_index += len(self.mecab_result[mecab_index][0]) # 단어 이동
                plaintext_index,_ = self.plaintext_index_move(plaintext_index)
                mecab_index += 1
                self.compound_noun = ""
        
        return self.compound_noun_list

    def result_compound_list(self):
        """
        """
        result_list = [ w for w in list(set(self.compound_noun_list)) if len(w) >= 2 ]
        print(result_list)

##################################
## ------------------------------
## MAIN FUNCTION START 
## ------------------------------
##################################
"""
if __name__ == "__main__":
    o = Nature(plaintext=p)
    o.get_nng()
    o.result_compound_list()
"""
