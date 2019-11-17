#
# 
# Run: python3 parse.py <file>.xml
#
# Takes input xml file, and outputs a xml file that only keeps sentences with the desired parts of speeches
#
# For this, the desired pos are VVN and VVD:
#   - VVD - The past tense form of lexical verbs (e.g. forgot, sent, lived, returned)
#   - VVN - The past participle form of lexical verbs (e.g. forgotten, sent, lived, returned)
#
#

import sys
import xml.etree.ElementTree as ET
# http://docs.python.org/library/xml.etree.elementtree.html


# Create tree, with only sentences from source tree
def get_sentences(src_tree):
  root = src_tree.getroot()     # root of source tree
  top = ET.Element('top')       # new root element
  tree = ET.ElementTree(top)    # new tree with new root

  # For all sentences in source tree, add it to new trew
  for s in root.findall(".//s"):
    top.append(s)

  return tree

# Deletes sentences that don't contain target parts of speech
def isolate_pos(src_tree):
  root = src_tree.getroot()

  parents = root.findall(".//s/..")   # elements that have <s> as children
  # For all elements with sentences
  for p in parents:
    # For each sentence
    for s in p.findall("./s"):
      keep = False    # default to sentence removal
      # For each word
      for w in s.findall("./w"):
        c5 = w.attrib['c5']       # c5 tag of word
        # If a word in the sentences has the desired tags, keep the sentence
        if c5 == 'VVN' or c5 == 'VVD':
          keep = True
          break
      # If not marked for keeping, remove the sentence
      if not keep:
        p.remove(s)
  return src_tree


def main(file):
  # Create ElementTree from input xml file
  try:
    src_tree = ET.parse(file)
    print(file)
    root = src_tree.getroot()
  except:
    # some exception handling thing, idk, unfinished
    return -1

  # Get target parts of speech, unfinished
  # try:
  #   pos[] = targets
  # except:
  #   # some exception handling thing, idk, unfinished
  #   return -1

  # Delete sentences without VVN or VVD words
  iso_tree = isolate_pos(src_tree)

  # Create new ElementTree w only sentences
  output = get_sentences(iso_tree)

  # Write to file
  output.write("post_"+file)

for arg in sys.argv[1:]:
  main(arg)

# if __name__ == "__main__":
#   sys.exit(main(sys.argv[1]))