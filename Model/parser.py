from pyvi import ViTokenizer
from Model.stack_ import Stack
from Model.queue_ import Queue
class Parser():
    def __init__(self):
        self.wordtype_relation = {'V_N': ['sub', 'loc', 'tmp'],
                                     'N_P': ['nmod'],
                                     'CH_V': ['root'],
                                     'N_Np': ['nmod'],
                                     'N_M': ['det'],
                                     'V_CH': ['punct'],
                                     'CH_N': ['root'],
                                     'N_N': ['nmod'],
                                     'N_E': ['loc'],
                                     'E_Np': ['pob'],
                                     'E_E': ['pmod'],
                                     #'N_CH': ['punct'],
                                     'N_L': ['det'],
                                     'V_E': ['dir', 'loc'],
                                     'E_N': ['pob'],
                                     'ROOT_V': ['root']}
        
        self.head_relation = ['root',
                             'đến',
                             'xe_buýt',
                             '?',
                             'thành_phố',
                             'lúc',
                             'thời_gian',
                             'từ',
                             'xe',
                             'đi',
                             'xuất_phát',
                             'bus']
        
        self.word_dict      = {'xe_buýt': {'posTag': ['N'], 'depLabel': ['sub', 'nmod']},
                                 'nào': {'posTag': ['P'], 'depLabel': ['nmod']},
                                 'đến': {'posTag': ['V', 'E'], 'depLabel': ['root', 'dir', 'pmod']},
                                 'thành_phố': {'posTag': ['N'], 'depLabel': ['loc', 'pob']},
                                 'huế': {'posTag': ['Np'], 'depLabel': ['nmod', 'pob']},
                                 'lúc': {'posTag': ['N'], 'depLabel': ['tmp']},
                                '2000hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '1000hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '1200hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '1230hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '1330hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '1400hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '1730hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '1900hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '2030hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '2200hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '2230hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '400hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '500hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '530hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '830hr': {'posTag': ['M'], 'depLabel': ['det']},
                                '930hr': {'posTag': ['M'], 'depLabel': ['det']},
                                 '?': {'posTag': ['CH'], 'depLabel': ['punct']},
                                 'thời_gian': {'posTag': ['N'], 'depLabel': ['root']},
                                 'b3': {'posTag': ['Np'], 'depLabel': ['nmod']},
                                 'b1': {'posTag': ['Np'], 'depLabel': ['nmod']}, 
                                 'b2': {'posTag': ['Np'], 'depLabel': ['nmod']}, 
                                 'b4': {'posTag': ['Np'], 'depLabel': ['nmod']}, 
                                 'b5': {'posTag': ['Np'], 'depLabel': ['nmod']},
                                 'b6': {'posTag': ['Np'], 'depLabel': ['nmod']}, 
                                 'b7': {'posTag': ['Np'], 'depLabel': ['nmod']}, 
                                 'từ': {'posTag': ['E'], 'depLabel': ['loc']},
                                 'đà_nẵng': {'posTag': ['Np'], 'depLabel': ['pob']},
                                 'xe': {'posTag': ['N'], 'depLabel': ['sub']},
                                 'bus': {'posTag': ['N'], 'depLabel': ['nmod']},
                                 'hồ_chí_minh': {'posTag': ['Np'], 'depLabel': ['nmod']},
                                 'những': {'posTag': ['L'], 'depLabel': ['det']},
                                 'đi': {'posTag': ['V'], 'depLabel': ['root']},
                                 'xuất_phát': {'posTag': ['V'], 'depLabel': ['root']},
                                 'root': {'posTag': ['ROOT'], 'depLabel': ['root']}}
        self.Question_words = ['nào']
    def makeleftarc(self,queue_head,queue,stack_head,stack,relation,rela_type,root_word):
        #queue.dequeue()
        stack.pop()
        relation.append( {
            'head' : queue_head,
            'word' : stack_head,
            'relationtype':rela_type
        } )

        
    def makerightarc(self,queue_head,queue,stack_head,stack,relation,rela_type,root_word):
        queue.dequeue()
        relation.append( {
            'head' : stack_head,
            'word' : queue_head, 
            'relationtype':rela_type
        } )

        ### check head word 
        if queue_head in self.head_relation :        
            stack.push(queue_head)
        else:
            if queue_head == 'huế' or queue_head == 'hồ_chí_minh' or queue_head == 'đà_nẵng':
                    while stack.getHead() != root_word and stack.getHead() != 'từ':
                        stack.pop()
                    if stack.getHead() == 'từ':
                        stack.pop()                       
    
    def check_replation(self,stack_head,queue_head):
        for lex_stack in self.word_dict[stack_head]['posTag']:
            for lex_queue in self.word_dict[queue_head]['posTag']:
                
                if lex_stack + "_" + lex_queue in self.wordtype_relation:
                    maybe_rel = list(set(self.wordtype_relation[lex_stack + "_" + lex_queue]) & set(self.word_dict[queue_head]['depLabel']))
                    if len(maybe_rel) >= 1 :
                        # LEFT ARC
                        return True, maybe_rel[0],  'r'
                
                if lex_queue + "_" + lex_stack in self.wordtype_relation :
                    maybe_rel = list(set(self.wordtype_relation[lex_queue + "_" + lex_stack]) & set(self.word_dict[stack_head]['depLabel']))
                    if len(maybe_rel) >= 1 :
                        # LEFT ARC
                        return True, maybe_rel[0],  'l'
                    
        return False,'_','_'

    def check_connetion(self,stack_head,relation):
        count = 0
        for rel_ in relation:
            if rel['head'] == stack_head:
                count += 1
            if rel['word'] == stack_head:
                count += 1
        if count >= 2 :
            return False
        else:
            return True
            
    def parsing(self,question):
        tokenized_question = ViTokenizer.tokenize(question.replace("bus","buýt").replace(":", "")).lower()
        ques_word_segment = tokenized_question.split()
        print(ques_word_segment)
        ## INIT ## 
        stack = Stack()
        queue = Queue()

        relation = []
        stack.push('root')
        root_word = None
    
        for word in ques_word_segment:
            queue.enqueue(word)
        
        while queue.length != 0 :
            #print("=======================================================")
            
            stack_head = stack.getHead()
            queue_head = queue.getHead()
            #print("VIS",stack_head,queue_head)
            #print(self.check_replation(stack_head,queue_head))
            if queue_head == '?' and root_word != None:
                while stack_head != root_word:
                    stack_head = stack.pop()   
            
            have_relation, rela_type , action = self.check_replation(stack_head,queue_head)
            #print(action)
            if have_relation and action == 'l':
                self.makeleftarc(queue_head,queue,stack_head,stack,relation,rela_type,root_word)
                #print('LARC',relation)
                continue 

            if have_relation and action == 'r':
                if rela_type == 'root' and root_word == None :
                    root_word = queue_head
                    #print('hjhjhjhbjhbb',root_word)
                elif rela_type == 'root' and root_word != None:
                    continue
                    
                self.makerightarc(queue_head,queue,stack_head,stack,relation,rela_type,root_word)
                #print('RARC',relation)
                continue
            
            
            # NO RELATION --> SHIFT
            if stack_head != 'thời_gian':
                queue.dequeue()
                stack.push(queue_head)
            else:
                # REDUCE
                stack.pop()
      
        return relation 