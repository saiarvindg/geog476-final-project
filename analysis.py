import pandas as pd
import geopandas as gp
import numpy as np
import os.path as path
import matplotlib.pyplot as plt
import rasterstats as rs
import scipy.stats
import matplotlib
import numpy as np

stateNameToCensusTractNum = {'RI':44}
nlcdComponents = []

class Analysis:
	
	def __init__(self, censusTractFile : str, landCoverFile : str, imperviousFile : str) -> None:
		from functools import reduce 
		# check if all files exist
		if reduce(lambda x,y: (x and path.isfile(y)), [censusTractFile, landCoverFile, imperviousFile], True):
			self.censusTractFile = censusTractFile
			self.landCoverFile = landCoverFile
			self.imperviousFile = imperviousFile
			print("Reading in National Census Tract Data...")
			self.nationalCensusTractsGDF = gp.read_file(self.censusTractFile)
			#self.imperviousRaster = rasterio.open(self.imperviousFile)
			#self.landCoverRaster = rasterio.open(self.landCoverFile)
			#self.impBand = self.imperviousRaster.read(1)
			#print(self.imperviousRaster.crs)
			#self.landCoverBand = self.landCoverRaster.read(1)
			self.calcPopDensityAndLandCoverPercents()
		else:
			raise ValueError('Please provide valid file name and paths')

	def calcPopDensityAndLandCoverPercents(self) -> None:
		# calculate the population densities and land cover percentages
		#print("Calculating Imprevious Surface Cover Percentage...")
		#self.calcImperviousSurfaceCoverPercentage()
		#print("Calculating Land Cover Percentages...")
		#self.calcNLCDComponentsPercentages()
		print("Calculating Population Density...")
		self.calcPopulationDensity()

	# NOTE: I think we should leave any graphing outside this class (i.e. just give them the data frame)
	#Sai
	def performPearsonAnalysisForState(self) -> (gp.GeoDataFrame,str, int):
		""" Performs the analysis and return the GeoDataFrame and R value """
		print("Performing Pearson analysis for census tract number: " + self.censusTractNum)
		
		self.calcPearsonCorrelationForImperviousLandCover()
		self.calcPearsonCorrelationForNLCDComponents()
		self.landCoverWithHighestR = getLandCoverTypeWithHighestR()
		
		return (self.stateCensusTract, self.landCoverWithHighestR[0], self.landCoverWithHighestR[1])

	#Sai
	def setCensusTractDataFrameForState(self, state : str):
		""" Get the census tracts for the specific state """
		#assigned state variable -Devin
		self.state = state
		# check if the state user provided is valid
		if state in stateNameToCensusTractNum:
			# first set the census tract number
			self.censusTractNum = stateNameToCensusTractNum[state]

			# use GeoPandas to clean up the data frame
			# TODO: select only the columns we need
			#I added geometry, land area as needed columns -Devin
			colNames = ['GEOID10','DP0010001','geometry','ALAND10']
			#convert square meters to square miles -Devin
			self.nationalCensusTractsGDF['ALAND10'] *= 3.8610215854245E-7
			self.stateCensusTractGDF = self.nationalCensusTractsGDF[colNames]
			# select only the census tract rows we need
			# creating filter
			self.stateCensusTractGDF = self.stateCensusTractGDF[self.stateCensusTractGDF['GEOID10'].str.startswith(str(self.censusTractNum))]
			self.stateCensusTractGDF = self.stateCensusTractGDF.to_crs({'init': 'epsg:5070'})
		else:
			raise TypeError('Please pass in a valid state abbrevation')

	#Valeria
	def calcPopulationDensity(self) -> None:
		""" Calcluate the populaiton density and add a column to the censusTractsGDF """
		# selecting rows that correspond with the state
		# selected_state= self.nationalCensusTractsGDF[self.nationalCensusTractsGDF.STATE_FIPS=  ]
		# sums_population_area= selected_state.sum(axis=0)
		# pop_density_calclulated= sums_population_area.DP001001/sums_population_area.LAND_AREA
		# adding new col?
		# self.nationalCensusTractsGDF['Population Density']=None
	
	#Devin 
	def calcImperviousSurfaceCoverPercentage(self) -> None:
		'''
		Calculate the impervious surface cover percentage using the censusTractsGDF. 
		Add the calculations to the censusTractsGDF as a column called "impervious_mean"
		'''
		#add population density column for census tracts        
		self.stateCensusTractGDF['pop_density'] = self.stateCensusTractGDF['DP0010001']/self.stateCensusTractGDF['ALAND10']
		self.impervious_stats = rs.zonal_stats(self.stateCensusTractGDF, self.imperviousFile, prefix = "impervious_", stats = 'mean', geojson_out = True)
		self.stateCensusTractGDF = gp.GeoDataFrame.from_features(self.impervious_stats)
		#read these variables into lists so that scipy can determine statistics
		pop_density_list = self.stateCensusTractGDF['pop_density'].tolist()
		impervious_mean_list = self.stateCensusTractGDF['impervious_mean'].tolist()
		#need to remove nan values
		pop_density_list = np.array(pop_density_list)
		pop_density_list = np.nan_to_num(pop_density_list)
		impervious_mean_list = np.array(impervious_mean_list)
		impervious_mean_list = np.nan_to_num(impervious_mean_list)
		#linear regression stats
		slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(pop_density_list, impervious_mean_list)
		self.plotImperviousRegression(pop_density_list, impervious_mean_list, r_value, intercept, slope)
		plt.show()
	#Devin
	def calcNLCDComponentsPercentages(self) -> None:
		"""
		For each land cover type - loop through, calculate, and add the percentage
		of each land cover type to the censusTractsGDF
		"""
		#finds pixel count so that percentages can be determined        
		self.nlcd_count = rs.zonal_stats(self.stateCensusTractGDF, self.landCoverFile, prefix = 'nlcd', stats = 'count', geojson_out = True)
		self.stateCensusTractGDF = gp.GeoDataFrame.from_features(self.nlcd_count)    
		#cmap is a legend corresponding pixels to classes
		cmap = {21: 'developed', 22: 'developed', 23: 'developed', 24: 'developed', 81: 'planted', 82: 'planted', 31:'barren', 
		       41: 'forest', 42: 'forest', 43: 'forest', 51:'shrubland', 52:'shrubland', 71:'herbaceous', 72:'herbaceous',
		       73:'herbaceous', 74:'herbaceous', 90:'wetlands', 95:'wetlands', 11:'water'}
		self.nlcd_stats = rs.zonal_stats(self.stateCensusTractGDF, self.landCoverFile, categorical = True, category_map = cmap, geojson_out = True)
		self.stateCensusTractGDF = gp.GeoDataFrame.from_features(self.nlcd_stats)
		#changes NaN to 0
		self.stateCensusTractGDF = self.stateCensusTractGDF.fillna(0)
        
		land_covers = []
		for key in cmap:
			if cmap[key] not in land_covers:
				 land_covers.append(cmap[key])       
		for i in land_covers:
			if i in self.stateCensusTractGDF.columns:
				self.stateCensusTractGDF[i] = self.stateCensusTractGDF[i]/self.stateCensusTractGDF['nlcdcount']           
		#TODO: i need to divide the land cover columns by the nlcd count col to get the percentage land cover
	def plotImperviousRegression(self, pop_density, percent_impervious, r, intercept, slope):
		plt.style.use('seaborn-darkgrid')

		#scatter plot of points
		plt.scatter(pop_density, percent_impervious, color = '#31a354',
                    edgecolors = 'black')
		print(slope, intercept, r**2)
		legend_label = matplotlib.patches.Patch(color='none', 
                                      label='y = {:.4f}x + {:.4f}, R$^2$ = {:.4f}'.format(slope, intercept, r**2))
		plt.legend(handles=[legend_label])

		#line = slope * pop_density + intercept
		#plt.plot(pop_density, line, 'r', zorder = 5, 
        	#label='y = {:.2f}x + {:.2f}, R$^2$ = {:.2f}'.format(slope, intercept, r**2), 
        	#color = '#984ea3', linewidth = 2.5)
		plt.xlabel('People per square mile')
		plt.ylabel('Percent Imperviousness')
		plt.title('Percent Imperviousness vs. Pop Density'.format(self.state))	
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

#test cases
census = r'./ri_census_tracts/ri_census_tracts.shp'
imp = r'./ri_imp6.tif'
nlcd = r'./ri_nlcd4.tif'
a = Analysis(census, nlcd, imp)
a.setCensusTractDataFrameForState("RI")
a.stateCensusTractGDF.plot()
a.calcImperviousSurfaceCoverPercentage()

a.calcNLCDComponentsPercentages()
a.stateCensusTractGDF.head() 
