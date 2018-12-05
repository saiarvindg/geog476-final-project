import pandas as pd
import geopandas as gp
import numpy as np
import os.path as path
import matplotlib.pyplot as plt
import rasterstats as rs
import scipy.stats
import matplotlib
import numpy as np
import sklearn.linear_model

stateNameToCensusTractNum = {'RI':'44','NY':'36','FL':'12','WI':'55','CA':'06','NE':'31'}
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
		else:
			raise ValueError('Please provide valid file name and paths')

	def calcPopDensityAndLandCoverPercents(self) -> None:
		# calculate the population densities and land cover percentages
		print("Calculating Imprevious Surface Cover Percentage...")
		self.calcImperviousSurfaceCoverPercentage()
		print("Calculating Land Cover Percentages...")
		self.calcNLCDComponentsPercentages()
		print("Calculating Population Density...")
		self.calcStatePopulationDensity()

	# NOTE: I think we should leave any graphing outside this class (i.e. just give them the data frame)
	#Sai
	def performPearsonAnalysis(self) -> None:
		""" Performs the analysis and return the GeoDataFrame and R value """
		print("Performing Pearson analysis for census tract number: " + self.censusTractNum)
		self.calcPearsonForImpervious()
		self.calcPearsonForLandCover()

	def performMultLinRegAnalysis(self) -> None:
		""" Performs the analysis and return the GeoDataFrame and R value """
		print("Performing Multiple Linear Regression analysis for census tract number: " + self.censusTractNum)
		self.calcMultLinReg()	
	
	
	def calcPearsonForImpervious(self) -> None:
		#read these variables into lists so that scipy can determine statistics
		pop_density_list = self.stateCensusTractGDF['pop_density'].tolist()
		impervious_mean_list = self.stateCensusTractGDF['impervious_mean'].tolist()
		#need to remove nan values
		pop_density_list = np.array(pop_density_list)
		self.pop_density_list = np.nan_to_num(pop_density_list)
		impervious_mean_list = np.array(impervious_mean_list)
		impervious_mean_list = np.nan_to_num(impervious_mean_list)
		#linear regression stats
		slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(self.pop_density_list, impervious_mean_list)

		self.plotRegression(self.pop_density_list, impervious_mean_list, r_value, intercept, slope, "impervious")
		plt.show()

	def calcPearsonForLandCover(self) -> None:
		for i in self.land_covers:
			if i in self.stateCensusTractGDF.columns:
				#calculate percent land cover
				#need to divide the land cover columns by the nlcd count col to get the percentage land cover
				lc_mean_list = self.stateCensusTractGDF[i].tolist()
				lc_mean_list = np.array(lc_mean_list)
				lc_mean_list = np.nan_to_num(lc_mean_list)
				slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(self.pop_density_list, 
                                                                                     lc_mean_list)
				self.plotRegression(self.pop_density_list, lc_mean_list, r_value, intercept, slope, i)
				plt.show()

	def calcMultLinReg(self) -> None:
		#read these variables into lists so that scipy can determine statistics
		pop_density_list = self.stateCensusTractGDF['pop_density'].tolist() # Y
		impervious_mean_list = self.stateCensusTractGDF['impervious_mean'].tolist() # X1
		developed_list = self.stateCensusTractGDF['developed'].tolist() # X2
		planted_list = self.stateCensusTractGDF['planted'].tolist() # X3
		
		#need to remove nan values
		pop_density_list = np.array(pop_density_list)
		self.pop_density_list = np.nan_to_num(pop_density_list)

		impervious_mean_list = np.array(impervious_mean_list)
		impervious_mean_list = np.nan_to_num(impervious_mean_list)

		developed_list = np.array(developed_list)
		developed_list = np.nan_to_num(developed_list)

		planted_list = np.array(planted_list)
		planted_list = np.nan_to_num(planted_list)

		print("pop density: " + str(len(self.pop_density_list)))
		print("impervious_mean_list: " + str(len(impervious_mean_list)))
		print("developed_list: " + str(len(developed_list)))
		print("planted_list: " + str(len(planted_list)))


		#linear regression stats
		landcovers = [impervious_mean_list, developed_list, planted_list]
		regr = sklearn.linear_model.LinearRegression()
		# regr = regr.fit(landcovers, self.pop_density_list)
		regr = regr.fit(self.stateCensusTractGDF[["impervious_mean","developed","planted"]], self.pop_density_list)
		r2_value = regr.score(landcovers, self.pop_density_list)
		print("mult. lin. reg r2 value: " + str(r2_value))
		intercept = regr.intercept_
		print("mult. lin. reg intercept: " + str(intercept))
		slope = regr.coeff_
		print("mult. lin. reg. coefficient: "  + str(slope))
		regr.predict(landcovers)
		print("mult. lin. reg get_params: " + str(regr.get_params()))
		pred = regr.predict(landcovers)
		print("muilt. lin. reg prediction: "  + str(pred))

		# self.plotRegression(self.pop_density, None, r2_value, intercept, slope, None, False)
		# plt.show()
	

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
			self.stateCensusTractGDF = self.stateCensusTractGDF[self.stateCensusTractGDF['GEOID10'].str.startswith(self.censusTractNum)]

			#crs data is shown as a proj 4 string 

			#Reprojected. crs data is shown as a proj 4 string -Devin
			self.stateCensusTractGDF = self.stateCensusTractGDF.to_crs('+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs')
			self.calcPopDensityAndLandCoverPercents()
		else:
			raise TypeError('Please pass in a valid state abbrevation')

	#Valeria
	def calcStatePopulationDensity(self) -> None:
		""" Calcluate the populaiton density and add a column to the censusTractsGDF """
		# selecting rows that correspond with the state
		sumPopArea = self.stateCensusTractGDF['DP0010001'].sum(axis=0)
		sumLandArea = self.stateCensusTractGDF['ALAND10'].sum(axis=0)
		# sums_population_area= self.state.sum(axis=0)
		# pop_density_calclulated= sums_population_area.DP001001/sums_population_area.LAND_AREA
		popDensityCalculated = sumPopArea / sumLandArea
		# adding new col
		# self.nationalCensusTractsGDF['Population Density']=None
		self.nationalCensusTractsGDF['statePopDensity'] = popDensityCalculated
	
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

	#Devin
	def calcNLCDComponentsPercentages(self) -> None:
		"""
		For each land cover type - loop through, calculate, and add the percentage
		of each land cover type to the censusTractsGDF
        Because this analysis is based on population density it should be called after calcImperviousSurfaceCoverPercentage
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
       
		self.land_covers = []
		#dictionary will contain land cover classes, their r^2 values associated with pop density
		self.land_cover_stats = {}
		for key in cmap:
			if cmap[key] not in self.land_covers:
				self.land_covers.append(cmap[key])
		#divide the land cover classes by the total nmber of land cover pixels to determine land cover percentage for that census tract                    
		for i in self.land_covers:
			if i in self.stateCensusTractGDF.columns:
				#calculate percent land cover
				#divide the land cover columns by the nlcd count col to get the percentage land cover
				self.stateCensusTractGDF[i] = 100 * self.stateCensusTractGDF[i]/self.stateCensusTractGDF['nlcdcount']

	def plotRegression(self, pop_density, percent_landcover, r, intercept, slope, lc_type, pearson=True):
		plt.style.use('seaborn-darkgrid')

		if pearson:
			#scatter plot of points
			plt.scatter(pop_density, percent_landcover, color = '#31a354',
						edgecolors = 'black')
			line = pop_density * slope + intercept
			plt.plot(pop_density, line, 'r', zorder = 5, 
					label='y = {:.2f}x + {:.2f}, R$^2$ = {:.2f}'.format(slope, intercept, r**2), 
					color = '#377eb8', linewidth = 2.5)
			plt.legend()
			plt.xlabel('People per square mile')
			plt.ylabel('Percent {}'.format(lc_type))
			plt.title('Percent {} vs. Pop Density in {}'.format(lc_type, self.state))
			plt.savefig('./figures/{}_{}_pearson.png'.format(self.state, lc_type), dpi=250)
		else:
			pass
			# plt.savefig('./figures/{}_linreg.png'.format(self.state), dpi=250)