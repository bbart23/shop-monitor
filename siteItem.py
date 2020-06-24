class SiteItem:
	Name = ""
	Color = ""
	SoldOut = False
	Price = ""
	Sizes = ""

	def __init__(self, name, color, soldout):
		self.Name = name
		self.Color = color
		self.SoldOut = soldout
		self.Price = ""
		self.Sizes = ""