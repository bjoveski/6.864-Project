class PostHistoryItem:
  def __init__(self, elem):
    self.id = int(elem.attrib["Id"])
    self.postId = int(elem.attrib["PostId"])
    self.postHistoryTypeId = int(elem.attrib["PostHistoryTypeId"])
    self.text = elem.attrib.get("Text")
    self.closeReasonId = elem.attrib.get("CloseReasonId")
    






'''
unix scripts:
extract PostId from postshistory whose CloseReasonId=1

grep CloseReasonId=\"1\" posthistory.xml | cut  -d " " -f 6 | cut -d \" -f 2

####


'''