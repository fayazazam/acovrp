#!python2

import re

class TSPLIBParser(object):

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
		re_spec = r"(\w+)\s?\:\s?(.+)\n"

		sections = dict.fromkeys(['node_coords', 'depots', 'demands', 'edge_data', 'fixed_edges', 'display_data', 'tours', 'edge_weights',], False)

		with open(self.filename, 'r') as file:
			for line in file:
				if re.match(re_spec, line):
					m = re.match(re_spec, line)
					if m.group(1) == 'NAME':
						self.data['name'] = m.group(2)
					elif m.group(1) == 'TYPE':
						assert m.group(2) in TSPLIBParser.TYPES
						self.data['type'] = m.group(2)
					elif m.group(1) == 'COMMENT':
						self.data['comment'] = m.group(2)
					elif m.group(1) == 'DIMENSION':
						self.data['dimension'] = int(m.group(2))
					elif m.group(1) == 'CAPACITY':
						self.data['capacity'] = int(m.group(2))
					elif m.group(1) == 'EDGE_WEIGHT_TYPE':
						assert m.group(2) in TSPLIBParser.EDGE_WEIGHT_TYPES
						self.data['edge_weight_type'] = m.group(2)
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

				# if any(section in sections):
				# 	if sections['node_coords']:
						
				# else:					
				# 	line = line.split("\n")[0] # remove line feed at the end
				# 	line = line.split(": ", 1) # split on colon
				# 	if len(line) == 2:
				# 		if 'NAME' in line[0]:
				# 			self.data['name'] = line[1]
				# 		elif 'EDGE_WEIGHT_TYPE' in line[0]:
				# 			for EDGE_WEIGHT_TYPE in TSPLIBParser.EDGE_WEIGHT_TYPES:
				# 				if EDGE_WEIGHT_TYPE in line[1]:
				# 					self.data['edge_weight_type'] = EDGE_WEIGHT_TYPE
				# 		elif 'TYPE' in line[0]:
				# 			for TYPE in TSPLIBParser.TYPES:
				# 				if TYPE in line[1]:
				# 					self.data['type'] = TYPE
				# 		elif 'COMMENT' in line[0]:
				# 			self.data['comment'] = line[1]
				# 		elif 'DIMENSION' in line[0]:
				# 			self.data['dimension'] = int(line[1])
				# 		elif 'CAPACITY' in line[0]:
				# 			self.data['capacity'] = int(line[1])
				# 		elif 'EDGE_WEIGHT_FORMAT' in line[0]:
				# 			for EDGE_WEIGHT_FORMAT in TSPLIBParser.EDGE_WEIGHT_FORMATS:
				# 				if EDGE_WEIGHT_FORMAT in line[1]:
				# 					self.data['edge_weight_format'] = EDGE_WEIGHT_FORMAT
				# 		elif 'EDGE_DATA_FORMAT' in line[0]:
				# 			for EDGE_DATA_FORMAT in TSPLIBParser.EDGE_DATA_FORMATS:
				# 				if EDGE_DATA_FORMAT in line[1]:
				# 					self.data['edge_data_format'] = EDGE_DATA_FORMAT
				# 		elif 'NODE_COORD_TYPE' in line[0]:
				# 			for NODE_COORD_TYPE in TSPLIBParser.NODE_COORD_TYPES:
				# 				if NODE_COORD_TYPE in line[1]:
				# 					self.data['node_coord_type'] = NODE_COORD_TYPE
				# 		elif 'DISPLAY_DATA_TYPE' in line[0]:
				# 			for DISPLAY_DATA_TYPE in TSPLIBParser.DISPLAY_DATA_TYPES:
				# 				if DISPLAY_DATA_TYPE in line[1]:
				# 					self.data['display_data_type'] = DISPLAY_DATA_TYPE
				# 	elif len(line) == 1:
				# 		if 'EOF' in line:
				# 			break;
				# 		elif 'NODE_COORD_SECTION' in line:
				# 			sections['node_coords'] = True
				# 		elif 'DEPOT_SECTION' in line:
				# 			sections['depots'] = True
				# 		elif 'DEMAND_SECTION' in line:
				# 			sections['demands'] = True
				# 		elif 'EDGE_DATA_SECTION' in line:
				# 			sections['edge_data'] = True
				# 		elif 'FIXED_EDGES_SECTION' in line:
				# 			sections['fixed_edges'] = True
				# 		elif 'DISPLAY_DATA_SECTION' in line:
				# 			sections['display_data'] = True
				# 		elif 'TOUR_SECTION' in line:
				# 			sections['tours'] = True
				# 		elif 'EDGE_WEIGHT_SECTION' in line:
				# 			sections['edge_weights'] = True

					
		return self.data
