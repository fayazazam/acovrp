#!python2

import math
import re

class TSPLIBParser(object):

	@staticmethod
	def d_euc2d(i, j):
		xd = i[0] - j[0]
		yd = i[1] - j[1]
		return int(round(math.sqrt(xd*xd + yd*yd)))

	KEYS_SPEC = ['NAME', 'TYPE', 'COMMENT', 'DIMENSION', 'CAPACITY', 'EDGE_WEIGHT_TYPE', 'EDGE_WEIGHT_FORMAT', 'EDGE_DATA_FORMAT', 'NODE_COORD_TYPE', 'DISPLAY_DATA_TYPE', 'EOF']
	KEYS_DATA = ['NODE_COORD_SECTION', 'DEPOT_SECTION', 'DEMAND_SECTION', 'EDGE_DATA_SECTION', 'FIXED_EDGES_SECTION', 'DISPLAY_DATA_SECTION', 'TOUR_SECTION', 'EDGE_WEIGHT_SECTION']
	TYPES = ['TSP', 'ATSP', 'SOP', 'HCP', 'CVRP', 'TOUR']
	EDGE_WEIGHT_TYPES = ['EXPLICIT', 'EUC_2D', 'EUC_3D', 'MAX_2D', 'MAX_3D', 'MAN_2D', 'MAN_3D', 'CEIL_2D', 'GEO', 'ATT', 'XRAY1', 'XRAY2', 'SPECIAL']
	EDGE_WEIGHT_FORMATS = ['FUNCTION', 'FULL_MATRIX', 'UPPER_ROW', 'LOWER_ROW', 'UPPER_DIAG_ROW', 'LOWER_DIAG_ROW', 'UPPER_COL', 'LOWER_COL', 'UPPER_DIAG_COL', 'LOWER_DIAG_COL']
	EDGE_DATA_FORMATS = ['EDGE_LIST', 'ADJ_LIST']
	NODE_COORD_TYPES = ['TWOD_COORDS', 'THREED_COORDS', 'NO_COORDS']
	DISPLAY_DATA_TYPES = ['COORD_DISPLAY', 'TWOD_DISPLAY', 'NO_DISPLAY']

	def __init__(self, filename):
		self.data = {}
		self.filename = filename

	def parse(self):
		re_spec = r'(\w+)\s*\:\s*([A-Z0-9\_]+)\s*\n'
		re_data = r'\s*([A-Z_]+)\s*\n'
		sections = dict.fromkeys(['node_coords', 'depots', 'demands', 'edge_data', 'fixed_edges', 'display_data', 'tours', 'edge_weights',], False)
		counter = 0

		with open(self.filename, 'r') as file:
			for line in file:
				if any(value for key, value in sections.iteritems()):
					if sections['node_coords']:
						try:
							counter += 1
							m = re.match(r'\s*(\d+)\s+(\-?\d+(\.\d+)?)\s+(\-?\d+(\.\d+)?)(\s+(\-?\d+(\.\d+)?))?\s*\n', line)
							if '2D' in self.data['edge_weight_type']:
								self.data['node_coord_section'].append(
									{'id': int(m.group(1)), 
									'x': float(m.group(2)), 
									'y': float(m.group(4))})
							elif '3D' in self.data['edge_weight_type']:
								self.data['node_coord_section'].append(
									{'id': int(m.group(1)), 
									'x': float(m.group(2)), 
									'y': float(m.group(4)), 
									'z': float(m.group(7))})
							else:
								print line
								raise ValueError('Invalid value for key \'edge_weight_type\'')
							assert counter < self.data['dimension']
						except AssertionError:
							counter = 0
							sections['node_coords'] = False
						except:
							print line
							raise
					elif sections['depots']:
						try:
							m = re.match(r'\s*(\d+)\s*\n', line)
							self.data['depot_section'].append(int(m.group(1)))
						except AttributeError:
							assert '-1' in line
							sections['depots'] = False
						except:
							print line
							raise
					elif sections['demands']:
						try:
							counter += 1
							m = re.match(r'\s*(\d+)\s+(\d+)\s*\n', line)
							self.data['demand_section'].append(
								{'id': int(m.group(1)),
								'demand': int(m.group(2))})
							assert counter < self.data['dimension']
						except AssertionError:
							counter = 0
							sections['demands'] = False
						except:
							print line
							raise
					elif sections['edge_data']:
						try:
							if self.data['edge_data_format'] == 'EDGE_LIST':
								m = re.match(r'\s*(\d+)\s+(\d+)\s*\n', line)
								self.data['edge_data_section'].append(
									(int(m.group(1)), int(m.group(2))))
							elif self.data['edge_data_format'] == 'ADJ_LIST':
								assert re.match(r'\s*(\d+)\s+(\d+\s+)+-1\s*\n', line)
								m = map(int, re.findall(r'\d+', line))
								self.data['edge_data_section'].append(
									{'id': m[0], 'adjacent': m[1:len(m)-1]})
							else:
								print line
								raise ValueError('Invalid value for key \'edge_data_format\'')
						except (AssertionError, AttributeError):
							assert '-1' in line
							sections['edge_data'] = False
						except:
							print line
							raise
					elif sections['fixed_edges']:
						try:
							m = re.match(r'\s*(\d+)\s+(\d+)\s*\n', line)
							self.data['fixed_edges_section'].append(
								(int(m.group(1)), int(m.group(2))))
						except AttributeError:
							assert '-1' in line
							sections['fixed_edges'] = False
						except:
							print line
							raise
					elif sections['display_data']:
						try:
							counter += 1
							m = re.match(r'\s*(\d+)\s+(\-?\d+(\.\d+)?)\s*(\-?\d+(\.\d+)?)\s*\n', line)
							self.data['display_data_section'].append(
								{'id': int(m.group(1)), 
								'x': float(m.group(2)), 
								'y': float(m.group(4))})
							assert counter < self.data['dimension']
						except AssertionError:
							counter = 0
							sections['display_data'] = False
						except:
							print line
							raise
					elif sections['tours']:
						try:
							assert re.match(r'\s*(\d+\s+)+', line)
							m = map(int, re.findall(r'\d+', line))
							for node_id in m:
								self.data['tour_section'].append(node_id)
						except AssertionError:
							assert '-1' in line
							sections['tours'] = False
						except:
							print line
							raise
					elif sections['edge_weights']:
						print 'edge_weights'
						sections['edge_weights'] = False
				else:					
					if re.match(re_spec, line):
						m = re.match(re_spec, line)
						if m.group(1) == 'NAME':
							self.data['name'] = m.group(2)
						elif m.group(1) == 'TYPE':
							TYPE = re.match(r'\s*(\w+)\s*', m.group(2))
							assert TYPE.group(1) in TSPLIBParser.TYPES
							self.data['type'] = TYPE.group(1)
						elif m.group(1) == 'COMMENT':
							self.data['comment'] = m.group(2)
						elif m.group(1) == 'DIMENSION':
							self.data['dimension'] = int(m.group(2))
						elif m.group(1) == 'CAPACITY':
							self.data['capacity'] = int(m.group(2))
						elif m.group(1) == 'EDGE_WEIGHT_TYPE':
							EDGE_WEIGHT_TYPE = re.match(r'\s*(\w+)\s*', m.group(2))
							assert EDGE_WEIGHT_TYPE.group(1) in TSPLIBParser.EDGE_WEIGHT_TYPES
							self.data['edge_weight_type'] = EDGE_WEIGHT_TYPE.group(1)
						elif m.group(1) == 'EDGE_WEIGHT_FORMAT':
							assert m.group(2) in TSPLIBParser.EDGE_WEIGHT_FORMATS
							self.data['edge_weight_format'] = m.group(2)
						elif m.group(1) == 'EDGE_DATA_FORMAT':
							assert m.group(2) in TSPLIBParser.EDGE_DATA_FORMATS
							self.data['edge_data_format'] = m.group(2)
						elif m.group(1) == 'NODE_COORD_TYPE':
							assert m.group(2) in TSPLIBParser.NODE_COORD_TYPES
							self.data['node_coord_type'] = m.group(2)
						elif m.group(1) == 'DISPLAY_DATA_TYPE':
							assert m.group(2) in TSPLIBParser.DISPLAY_DATA_TYPES
							self.data['display_data_type'] = m.group(2)
					elif re.match(re_data, line):
						m = re.match(re_data, line)
						if m.group(1) == 'EOF':
							break
						elif m.group(1) == 'NODE_COORD_SECTION':
							sections['node_coords'] = True
							self.data['node_coord_section'] = []
						elif m.group(1) == 'DEPOT_SECTION':
							self.data['depot_section'] = []
							sections['depots'] = True
						elif m.group(1) == 'DEMAND_SECTION':
							self.data['demand_section'] = []
							sections['demands'] = True
						elif m.group(1) == 'EDGE_DATA_SECTION':
							self.data['edge_data_section'] = []
							sections['edge_data'] = True
						elif m.group(1) == 'FIXED_EDGES_SECTION':
							self.data['fixed_edges_section'] = []
							sections['fixed_edges'] = True
						elif m.group(1) == 'DISPLAY_DATA_SECTION':
							self.data['display_data_section'] = []
							sections['display_data'] = True
						elif m.group(1) == 'TOUR_SECTION':
							self.data['tour_section'] = []
							sections['tours'] = True
						elif m.group(1) == 'EDGE_WEIGHT_SECTION':
							sections['edge_weights'] = True
		return self.data
