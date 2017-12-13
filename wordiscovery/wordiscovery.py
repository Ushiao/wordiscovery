# coding: utf-8

import math


class TrieNode(object):
    """TrieNode is node in trietree, each node contains parent of this node,
       node frequence, children, and all children frequence. this structure data
       for calculation
    """

    def __init__(self,
                 frequence=0,
                 children_frequence=0,
                 parent=None):
        self.parent = parent
        self.frequence = frequence
        self.children = {}
        self.children_frequence = children_frequence

    def insert(self, char):
        self.children_frequence += 1
        self.children[char] = self.children.get(char, TrieNode(parent=self))
        self.children[char].frequence += 1
        return self.children[char]

    def fetch(self, char):
        return self.children[char]


class TrieTree(object):
    def __init__(self, size=6):
        self._root = TrieNode()
        self.size = size

    def get_root(self):
        return self._root

    def insert(self, chunk):
        node = self._root
        for char in chunk:
            node = node.insert(char)
        if len(chunk) < self.size:
            # add symbol "EOS" at end of line trunck
            node.insert("EOS")

    def fetch(self, chunk):
        node = self._root
        for char in chunk:
            node = node.fetch(char)
        return node

# In[153]:


class WordDiscovery(object):
    def __init__(self, ngram_size=6):
        self.puncs = ['【','】',')','(','、','，','“','”',
                     '。','《','》',' ','-','！','？','.',
                     '\'','[',']','：','/','.','"','\u3000',
                     '’','．',',','…','?',';','·','%','（',
                     '#','）','；','>','<','$', ' ', ' ','\ufeff'] 
        
        self.fw_ngram = TrieTree(ngram_size)
        self.bw_ngram = TrieTree(ngram_size)
        self.ngram_size = ngram_size
        
    def preparse(self, text):
    
        # replace punctuaton wiht "\n"
        for punc in self.puncs:
            text = text.replace(punc, "\n")

        # Todo: Delimiter alphabetic string, number from chinese text
        #regex_num_alpha = re.compile()
        #text = re.sub(r"([a-zA-Z0-9]+)", r"\n\1", text, flags=re.M)

        chunks, bchunks = [], []
        
        # split text in to line
        for line in text.strip().split("\n"):
            line = line.strip()
            bline = line[::-1]
            for start in range(len(line)):
                # insert data into structure
                end = start + self.ngram_size
                chunk = line[start:end]
                bchunk = bline[start:end]
                self.fw_ngram.insert(chunk)
                self.bw_ngram.insert(bchunk)

                if len(chunk) == 6:
                    chunk = chunk[:-1]

                while len(chunk) > 1:
                    chunks.append(chunk)
                    bchunks.append(chunk[::-1])
                    chunk = chunk[:-1]

        return chunks, bchunks

    def calc_entropy(self, chunks, ngram):
        
        def entropy(sample, total):
            """Entropy"""
            s = float(sample)
            t = float(total)
            result = - s/t * math.log(s/t)
            return result
        
        def parse(chunk, ngram):
            node = ngram.fetch(chunk)
            total = node.children_frequence
            return sum([entropy(sub_node.frequence, 
                               total) for sub_node in node.children.values()])
        
        word2entropy = {}
        for chunk in chunks:
            word2entropy[chunk] = parse(chunk, ngram)   
        return word2entropy
                
    def calc_mutualinfo(self, chunks, ngram):
        """Mutual Information
        log(p(x,y)/(p(x)*p(y))) = log(p(y|x)/p(y))"""

        def parse(chunk, root):
            sub_node_y_x = ngram.fetch(chunk)
            node = sub_node_y_x.parent
            sub_node_y = root.children[chunk[-1]]
            
            prob_y_x = float(sub_node_y_x.frequence) / node.children_frequence
            prob_y = float(sub_node_y.frequence) / root.children_frequence
            mutualinfo = math.log(prob_y_x / prob_y)
            return mutualinfo, sub_node_y_x.frequence
        
        word2mutualinfo = {}  
        root = ngram.get_root()
        for chunk in chunks:
            word2mutualinfo[chunk] = parse(chunk, root)
        return word2mutualinfo
    
    def parse(self,
              text,
              entropy_threshold=0.8,
              mutualinfo_threshold=7,
              freq_threshold=10):
        chunks, bchunks = self.preparse(text)
        return self._fetch_final(chunks,
                          bchunks,
                          entropy_threshold,
                          mutualinfo_threshold,
                          freq_threshold
                         )

    def _fetch_final(self,
                     chunks,
                     bchunks,
                     entropy_threshold=0.8,
                     mutualinfo_threshold=7,
                     freq_threshold=10):
        fw_entropy = self.calc_entropy(chunks, self.fw_ngram)
        bw_entropy = self.calc_entropy(bchunks, self.bw_ngram)
        fw_mi = self.calc_mutualinfo(chunks, self.fw_ngram)
        bw_mi = self.calc_mutualinfo(bchunks, self.bw_ngram)

        final = {}
        for k, v in fw_entropy.items():
            if k[::-1] in bw_mi and k in fw_mi:
                mi_min = min(fw_mi[k][0], bw_mi[k[::-1]][0])
                word_prob = min(fw_mi[k][1], bw_mi[k[::-1]][1])
                if mi_min < mutualinfo_threshold:
                    continue
            else:
                continue
            if word_prob < freq_threshold:
                continue
            if k[::-1] in bw_entropy:
                en_min = min(v, bw_entropy[k[::-1]])
                if en_min < entropy_threshold:
                    continue
            else:
                continue
            final[k] = (word_prob, mi_min, en_min)
        return final

# In[155]:


def main(filename):
    with open(filename, "r") as inf:
        text = inf.read()
    f = WordDiscovery(6)
    word_info = f.parse(text,
                        entropy_threshold=0.001,
                        mutualinfo_threshold=4,
                        freq_threshold=3)
    for k, v in sorted(word_info.items(),
                       key=lambda x:x[1][0],
                       reverse=False):
        print("%+9s\t%-5d\t%.4f\t%.4f"%(k, v[0], v[1], v[2]))


if __name__ == "__main__":
    import os
    main(os.path.join("data",
                      "shijiuda.txt")
        )


