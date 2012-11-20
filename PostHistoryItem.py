class PostHistoryItem:
  def __init__(self, elem):
    self.id = int(elem.attrib["Id"])
    self.postId = int(elem.attrib["PostId"])
    self.postHistoryTypeId = int(elem.attrib["PostHistoryTypeId"])
    self.text = elem.attrib.get("Text")
    self.closeReasonId = elem.attrib.get("CloseReasonId")
    

