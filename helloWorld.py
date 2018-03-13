my_file = open("PressureCalibration-2018.txt", 'r')
my_file_offsets = open("1-PressureCalibration-2018-offsets.txt", 'w')
my_file_offsets_correct = open("2-PressureCalibration-2018-offsets-correct.txt", 'w')
my_file_daqsetup = open("daqSetup.cfg", 'r')
my_file_daqsetup_new = open("3-daqSetup-new.cfg", 'w')
# start with the calibration summands
count_lines = 0
calibration_offsets = [] # it has the calibration offset from all pressures
daqsetup_values = []
# we start reading the copy paste from matlab with the summands.
for line in my_file:
    current_line = str(line)
    if current_line != '\n' and len(current_line) >= 35:  # this should filter the first line
        variable = current_line[5:16]
        start_offset = int(current_line.index(":"))
        variable_offset = current_line[start_offset+1:-1]
        # if count_lines == 39:
        #     my_file_offsets.write("{0}, {1},\n".format(variable, variable_offset))
        #     calibration_offsets.append(int(variable_offset))
        # else:
        my_file_offsets.write("{0}, {1},\n".format(variable, variable_offset[:-1]))
        calibration_offsets.append(int(variable_offset[:-1]))
        count_lines += 1

# now we go for the daqsetup
offset_index = 0
for line in my_file_daqsetup:
    current_line = str(line)
    if "PA[0]" in current_line or "PB[0]" in current_line or \
       "PS[0]" in current_line or "PT[0]" in current_line or "DP[0]" in current_line:
        variable_offset = current_line.index("}{")
        if offset_index == 39:
            variable_value = int(current_line[variable_offset+2:-1])
            daqsetup_values.append(variable_value + calibration_offsets[offset_index])
            my_file_daqsetup_new.write(current_line[: variable_offset + 2] +
                                       str(daqsetup_values[offset_index]) + '}')
        else:
            variable_value = int(current_line[variable_offset + 2: -2])
            daqsetup_values.append(variable_value+ calibration_offsets[offset_index])
            my_file_daqsetup_new.write(current_line[: variable_offset + 2] +
                                       str(daqsetup_values[offset_index]) + '}\n')
        print(variable_value + calibration_offsets[offset_index])
        offset_index += 1
    else:
        my_file_daqsetup_new.write(current_line)
