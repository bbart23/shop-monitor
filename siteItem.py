class SiteItem:
	Name = ""
	Color = ""
	SoldOut = False
	Price = ""
	Sizes = ""
	Picture = ""
	Link = ""

	def __init__(self, name, color, soldout):
		self.Name = name
		self.Color = color
		self.SoldOut = soldout
		self.Price = ""
		self.Sizes = ""
		self.Picture = ""
		self.Link = ""