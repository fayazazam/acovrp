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
		re_spec = r"(\w+)\s*\:\s*(.+)\n"
		re_data = r"\s*([A-Z_]+)\s*\n"
		re_node_coords = r"\s*(\d+)\s+(\-?\d+(\.\d+)?)\s+(\-?\d+(\.\d+)?)\s*\n"
		sections = dict.fromkeys(['node_coords', 'depots', 'demands', 'edge_data', 'fixed_edges', 'display_data', 'tours', 'edge_weights',], False)
		counter = 0

		with open(self.filename, 'r') as file:
			for line in file:
				if any(value for key, value in sections.iteritems()):
					if sections['node_coords']:
						if counter < self.data['dimension']:
							m = re.match(re_spec, line)
							print m.group(2)
							counter += 1
							continue
						else:
							counter = 0
							sections['node_coords'] = False
					elif sections['depots']:
						print 'depots'
						sections['depots'] = False
					elif sections['demands']:
						print 'demands'
						sections['demands'] = False
					elif sections['edge_data']:
						print 'edge_data'
						sections['edge_data'] = False
					elif sections['fixed_edges']:
						print 'fixed_edges'
						sections['fixed_edges'] = False
					elif sections['display_data']:
						print 'display_data'
						sections['display_data'] = False
					elif sections['tours']:
						print 'tours'
						sections['tours'] = False
					elif sections['edge_weights']:
						print 'edge_weights'
						sections['edge_weights'] = False
				else:					
					if re.match(re_spec, line):
						m = re.match(re_spec, line)
						if m.group(1) == 'NAME':
							self.data['name'] = m.group(2)
						elif m.group(1) == 'TYPE':
							TYPE = re.match(r"\s*(\w+)\s*", m.group(2))
							assert TYPE.group(1) in TSPLIBParser.TYPES
							self.data['type'] = TYPE.group(1)
						elif m.group(1) == 'COMMENT':
							self.data['comment'] = m.group(2)
						elif m.group(1) == 'DIMENSION':
							self.data['dimension'] = int(m.group(2))
						elif m.group(1) == 'CAPACITY':
							self.data['capacity'] = int(m.group(2))
						elif m.group(1) == 'EDGE_WEIGHT_TYPE':
							EDGE_WEIGHT_TYPE = re.match(r"\s*(\w+)\s*", m.group(2))
							assert EDGE_WEIGHT_TYPE.group(1) in TSPLIBParser.EDGE_WEIGHT_TYPES
							self.data['edge_weight_types'] = EDGE_WEIGHT_TYPE.group(1)
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
						elif m.group(1) == 'DEPOT_SECTION':
							sections['depots'] = True
						elif m.group(1) == 'DEMAND_SECTION':
							sections['demands'] = True
						elif m.group(1) == 'EDGE_DATA_SECTION':
							sections['edge_data'] = True
						elif m.group(1) == 'FIXED_EDGES_SECTION':
							sections['fixed_edges'] = True
						elif m.group(1) == 'DISPLAY_DATA_SECTION':
							sections['display_data'] = True
						elif m.group(1) == 'TOUR_SECTION':
							sections['tours'] = True
						elif m.group(1) == 'EDGE_WEIGHT_SECTION':
							sections['edge_weights'] = True
		return self.data
