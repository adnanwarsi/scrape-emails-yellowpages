import csv
import glob
import re
import json


outcsvfile = "combined_large.csv"


with open(outcsvfile, "w", newline='') as output:
    record_writer = csv.writer(output, lineterminator='\n')

    # for jsonfile in glob.glob("*.json"):
    #
    #     jsonfile_category = jsonfile.split(".")[0]
    #     jsonfile_category = " ".join(re.split('-|_', jsonfile_category))
    #
    #     with open(jsonfile) as f:
    #         records_list = json.load(f)
    #         for record_num in range(0, len(records_list)-1):
    #             print (records_list[record_num])
    #
    #             records_list[record_num]["category"] = jsonfile_category
    #
    #             writer = csv.writer(output, lineterminator='\n')
    #             writer.writerow([records_list[record_num]['category'], records_list[record_num]['biz_name'], records_list[record_num]['address'], records_list[record_num]['phone'], records_list[record_num]['url'], records_list[record_num]['email']])

    for csvfilename in glob.glob("*.csv"):
        print (csvfilename)
        with open(csvfilename) as csvfile:
            jsonfile_category = csvfilename.split(".")[0]
            jsonfile_category = " ".join(re.split('-|_', jsonfile_category))

            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                row.insert(0,jsonfile_category)
                print(row)

                record_writer.writerow(row)

        csvfile.close()

output.close()