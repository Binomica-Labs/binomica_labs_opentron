#importing opentrons api
from opentrons import protocol_api

#metadata for description - Opentrons app will read from this protocol name and description, not the protocol file name!
metadata = {
	'protocolName': 'Beach sample dilution experiment',
	'author': 'Sung <sung@binomicalabs.org>',
	'description': 'Beach sample dilution with two makeshift plastic containers modeled after axygen reservoir',
	'apiLevel': '2.12'
}


#defining necessary equipment and their locations in the robot
def run(protocol: protocol_api.ProtocolContext):

	#labware
	tips = protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
	beach_sample = protocol.load_labware('axygen_1_reservoir_90ml', location='6')
	halomedia = protocol.load_labware('axygen_1_reservoir_90ml', location='5')
	plate = protocol.load_labware('corning_96_wellplate_360ul_flat', location='3')
	trash = protocol.load_labware('nest_1_reservoir_195ml', location='11')

	#pipette
	left_pipette = protocol.load_instrument('p300_single', mount='left', tip_racks=[tips])

	#experiment steps
	#fill in all of the 96 wells in 'plate' with location 5 diluent, the beach sample in this case
	#from left to right, 200ul is taken from 'beach_sample'. A1 simply denotes the reservoir itself. 'Plate' wells() indicate all available wells for the 'plate' location defined above
	#3x 100ul mixing step is performed before aspirating from the beach sample - this prevents solid residue carry over
	left_pipette.transfer(200, beach_sample['A1'], plate.wells(), mix_before=(3, 100))

	#defining range 8 for traveling down the column of the 'plate'
	#meanwhile halomedia (location 5) is dispensed from the reservoir to row 0 (python starts from 0)
	#the dilution in below step happens sequentially - halomedia is dispensed into row 0, and then the next line activates, dispending 100ul from row 0 and moving to the next row, and so on
	#when finished, due to 'range' the operation repeats on the row below the first operation
	for i in range(8):
		row = plate.rows()[i]
		left_pipette.transfer(100, halomedia['A1'], row[0], mix_after=(3, 50))
		left_pipette.transfer(100, row[:11], row[1:], mix_after=(3, 50))

	#Above loop method moves 100ul of each well from left to right - so last wells of each row (12th) would have 100ul more volume than the others.
	#we can use the transfer method here to point specific columns to a location, in this case another plastic container we're using as liquid collection trash
	#the destination here can be any other labware located in the robot - i.e. moving all column to one 6.9ml well in a 12 well plate for sample collection
	left_pipette.transfer(100, plate.columns_by_name() ['12'], trash['A1'])
