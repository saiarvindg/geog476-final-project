import GeoPandas as gp

class Analysis:
	stateNameToCensusTractNum = {'RI':44}
	nlcdComponents = []
	
	def __init__(self, stateName : str) -> None:
		self.stateName = stateName

		# extract census tracts and assign as instance
		self.censusTractsGDF = self.getCensusTracts()
		calcImperviousSurfaceCoverPercentage()
		calcLandCoverPercentages()
		self.landCoverWithHighestR = determineLandCoverTypeWithHighestR
	
	def getCensusTracts(self) -> gp.GeoDataFrame:
		""" Get the census tracts for each state """
		# TODO: use GeoPandas to select census tracts for the states
		return  # TODO: return GeoPandas data frame

	def calcPopulationDensity(self) -> None:
		""" Calcluate the populaiton density and add a column to the censusTractsGDF """
		#TODO: calculate the population density and add a column
	

	def calcImperviousSurfaceCoverPercentage(self) -> None:
		""" 
		Calculate the impervious surface cover percentage. Add the calculations
		to the censusTractsGDF
		"""
		#TODO: calculate the impervious surface cover percentage

		#TODO: add the calculations to self.censusTractsGDF

	def calcNLCDComponentsPercentages(self) -> None:
		"""
		For each land cover type - loop through, calculate, and add the percentage
		of each land cover type to the censusTractsGDF
		"""

		for landCover in ncldComponents:
			#TODO: calculate the percentage of the landCover for each census tract

			#TODO: add the land o column to census tract GDF
	
	def calcPearsonCorrelationForImperviousLandCover() -> None:
		""" 
		Calculate the Pearson correlation coefficient for population density and
		the impervious land cover 
		"""
		#TODO: calculate the Pearson correlation

		#TODO: add the land cover type and the r value to a dictionary in the class
		if self.landCoverPearsonCorrelations == None:
			self.landCoverPearsonCorrelations = {
				'impervious': #TODO: fill in the r value
			}
		else:
			self.landCoverPearsonCorrelations['impervious'] = #TODO: fill in the r value
	
	def calcPearsonCorrelationForNLCDComponents() -> None:
		""" 
		Calculate the Pearson correlation coefficient for population density and
		each of the NCLD components
		"""
		for landCover in ncldComponents:
			#TODO: calculate the Pearson correlation 

			#TODO: add the land cover type and the r value to a dictionary in the class
			if self.landCoverPearsonCorrelations == None:
				self.landCoverPearsonCorrelations = {
					landCover : #TODO: fill in the r value
				}
			else:
				self.landCoverPearsonCorrelations[landCover] = #TODO: fill in the r value

	def determineLandCoverTypeWithHighestR(self) -> Str:
		""" 
		Go through the landCoverPearsonCorrelations and get the land cover type 
		with the highest correlation
		"""
		#TODO: get the land cover type with the highest correlation
		return #TODO

	@staticmethod
	def getCensusTractNumberForState(state : str):
		return stateNameToCensusTractNum[state]

	

	