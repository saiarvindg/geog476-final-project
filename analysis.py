import pandas as pd
import geopandas as gp

class Analysis:
	stateNameToCensusTractNum = {'RI':44}
	nlcdComponents = []
	
	def __init__(self, censusTractFile, landCoverFile, imperviousFile, state : str) -> None:
		self.censusTractFile = censusTractFile
		self.landCoverFile = landCoverFile
		self.imperviousFile = imperviousFile
		self.censusTractsGDF = self.getCensusTracts()
	
	# NOTE: I think we should leave any graphing up to the user (i.e. just give them the data frame)
	def performPearsonAnalysisForState(self) -> (gp.GeoDataFrame,str, int):
		""" Performs the analysis and return the GeoDataFrame and R value """

		if state in stateNameToCensusTractNum:
			# extract census tracts and assign as instance
			calcImperviousSurfaceCoverPercentage()
			calcLandCoverPercentages()
			self.landCoverWithHighestR = getLandCoverTypeWithHighestR()
		else:
			raise TypeError('Please pass in a valid state abbrevation')

		
		return (self.censusTractsGDF, self.landCoverWithHighestR[0], self.landCoverWithHighestR[1])
	
	def getCensusTracts(self) -> gp.GeoDataFrame:
		""" Get the census tracts for each state """
		# TODO: use rasterio and GeoPandas to select census tracts for the states
		stateCensusTract = gp.read_file(r"../Tract_2010Census_DP1/Tract_2010Census_DP1.shp")
		stateCensusTract.head()
		return stateCensusTract

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
			pass
	
	def calcPearsonCorrelationForImperviousLandCover() -> None:
		""" 
		Calculate the Pearson correlation coefficient for population density and
		the impervious land cover 
		"""
		#TODO: calculate the Pearson correlation

		#TODO: add the land cover type and the r value to a dictionary in the class
		if self.landCoverPearsonCorrelations == None:
			#TODO
			"""
			self.landCoverPearsonCorrelations = {
				'impervious': fill in the r value
			}
			"""
			pass
		else:
			# self.landCoverPearsonCorrelations['impervious'] = #TODO: fill in the r value
			pass
	
	def calcPearsonCorrelationForNLCDComponents() -> None:
		""" 
		Calculate the Pearson correlation coefficient for population density and
		each of the NCLD components
		"""
		for landCover in ncldComponents:
			#TODO: calculate the Pearson correlation 

			#TODO: add the land cover type and the r value to a dictionary in the class
			if self.landCoverPearsonCorrelations == None:
				#TODO
				"""
				self.landCoverPearsonCorrelations = {
					landCover : fill in the r value
				}
				"""
			else:
				# self.landCoverPearsonCorrelations[landCover] = #TODO: fill in the r value
				pass

	def getLandCoverTypeWithHighestR(self) -> (str, int):
		""" 
		Go through the landCoverPearsonCorrelations and get the land cover type 
		and r value with the highest correlation
		"""
		#TODO: get the land cover type with the highest correlation
		"""
		return (
			#TODO: insert land cover type
			,
			#TODO: insert land cover type's r value
			)
		"""

	@staticmethod
	def getCensusTractNumberForState(state : str):
		return stateNameToCensusTractNum[state]

	

	