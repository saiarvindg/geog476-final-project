import pandas as pd
import geopandas as gp
import os.path as path

class Analysis:
	stateNameToCensusTractNum = {'RI':44}
	nlcdComponents = []
	
	def __init__(self, censusTractFile : str, landCoverFile : str, imperviousFile : str) -> None:
		import reduce from functools
		# check if all files exist
		if reduce(lambda x,y: (x and path.isfile(y)), [censusTractFile, landCoverFile, imperviousFile], True):
			self.censusTractFile = censusTractFile
			self.landCoverFile = landCoverFile
			self.imperviousFile = imperviousFile
		else:
			raise ValueError('Please provide valid file name and paths')
	
	# NOTE: I think we should leave any graphing outside this class (i.e. just give them the data frame)
	#Sai
	def performPearsonAnalysisForState(self, state : str) -> (gp.GeoDataFrame,str, int):
		""" Performs the analysis and return the GeoDataFrame and R value """

		# check if the state user provided is valid
		if state in stateNameToCensusTractNum:
			# first get the census tract data
			self.censusTractNum = stateNameToCensusTractNum[state]
			self.censusTractsGDF = self.getCensusTracts()

			# calculate the population densities and land cover percentages
			calcImperviousSurfaceCoverPercentage()
			calcLandCoverPercentages()
			calcPopulationDensity()
			self.landCoverWithHighestR = getLandCoverTypeWithHighestR()
		else:
			raise TypeError('Please pass in a valid state abbrevation')
		return (self.censusTractsGDF, self.landCoverWithHighestR[0], self.landCoverWithHighestR[1])

	#Sai
	def getCensusTracts(self) -> gp.GeoDataFrame:
		""" Get the census tracts for each state """
		# use GeoPandas to read in census tracts data for the states
		stateCensusTract = gp.read_file(self.censusTractFile)

		# TODO: select only the columns we need
		colNames = ['GEOID','DP0010001']
		stateCensusTract = stateCensusTract[colNames]

		# select only the census tract rows we need
		stateCensusTract = stateCensusTract[stateCensusTract.GEOID == self.censusTractNum]

		return stateCensusTract

	#Valeria
	def calcPopulationDensity(self) -> None:
		""" Calcluate the populaiton density and add a column to the censusTractsGDF """
		#TODO: calculate the population density and add a column
	
	#Devin 
	def calcImperviousSurfaceCoverPercentage(self) -> None:
		""" 
		Calculate the impervious surface cover percentage using the censusTractsGDF. 
		Add the calculations to the censusTractsGDF as a column
		"""
		#TODO: calculate the impervious surface cover percentage

		#TODO: add the calculations to self.censusTractsGDF
	#Devin
	def calcNLCDComponentsPercentages(self) -> None:
		"""
		For each land cover type - loop through, calculate, and add the percentage
		of each land cover type to the censusTractsGDF
		"""
		for landCover in ncldComponents:
			#TODO: calculate the percentage of the landCover for each census tract

			#TODO: add the land o column to census tract GDF
			pass
	#Daniel
	def calcPearsonCorrelationForImperviousLandCover() -> None:
		""" 
		Calculate the Pearson correlation coefficient for population density and
		the impervious land cover 
		"""
		#TODO: calculate the Pearson correlation using the censusTractsGDF

		#TODO: add the land cover type and the r value to a dictionary in the class
		if self.landCoverPearsonCorrelations == None:
			#TODO
			self.landCoverPearsonCorrelations = {
				'impervious': "fill in the r value"
			}

			pass
		else:
			# self.landCoverPearsonCorrelations['impervious'] = #TODO: fill in the r value
			pass
	#Daniel
	def calcPearsonCorrelationForNLCDComponents() -> None:
		""" 
		Calculate the Pearson correlation coefficient for population density and
		each of the NCLD components
		"""
		for landCover in ncldComponents:
			#TODO: calculate the Pearson correlation using the censusTractsGDF

			#TODO: add the land cover type and the r value to a dictionary in the class
			if self.landCoverPearsonCorrelations == None:
				#TODO
				self.landCoverPearsonCorrelations = {
					landCover : "fill in the r value"
				}
			else:
				# self.landCoverPearsonCorrelations[landCover] = #TODO: fill in the r value
				pass
	#Sai
	def getLandCoverTypeWithHighestR(self) -> (str, int):
		""" 
		Go through the landCoverPearsonCorrelations and get the land cover type 
		and r value with the highest correlation
		"""
		#TODO: get the land cover type with the highest correlation
		lc = max(self.landCoverPearsonCorrelations.keys(), key=(lambda k: self.landCoverPearsonCorrelations[k]))
		return (lc, self.landCoverPearsonCorrelations[lc])

	

	
