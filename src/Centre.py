class Centre():
	def __init__(self, cType, postCode, name, phone, suburb, providers):
		self._ctype = cType;
		self._postCode = postCode;
		self._name = name;
		self._phone = phone;
		self._suburb = suburb;
		self._providers = providers
		self._rating = []

	@property
	def ctype(self):
		return self._ctype

	@property
	def postCode(self):
		return self._postCode

	@property
	def name(self):
		return self._name

	@property
	def phone(self):
		return self._phone

	@property
	def suburb(self):
		return self._suburb

	@property
	def providers(self):
		return self._providers

	def append_prov_affil(self, provider):
		self._providers.append(provider)
	
	@property
	def get_rating(self):
		if not self._rating:
			return float(0)
		return round(float(sum(self._rating))/len(self._rating),1)

	def add_rating(self, rating):
		(self._rating).append(round(rating,1))