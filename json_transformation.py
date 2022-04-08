
import json
from os import remove
import re
import yaml
import requests

#Loads file to memory
""" with open("test3.json", "r") as fout2:
    json_data = json.load(fout2)
    for change in json_data["Changes"]:
        # strip the contents of trailing white spaces (new line)
        change["ResourceRecordSet"]["Name"] = "iwada"

# dump json to another file
with open("test3.json", "w") as fout:
    fout.write(json.dumps(json_data)) """

#Option does not load file to Memory
def fix_json(input_file,output_file):
    pattern = 'NumberInt.*$'
    with open(input_file, "r") as inp, open(output_file, "w") as out:
        for line in inp:
            if "NumberInt"  in line:
                #if line.endswith(","): # TODO - Check why does not work
                if "," in line:
                    #print(line)
                    line = re.sub(pattern, '"' + ("".join(filter(str.isdigit, line)) + '"' + ","), line)
                else:
                    line = re.sub(pattern, '"' + ("".join(filter(str.isdigit, line)) + '"'), line)
                    #print(line)
            out.write(line)

def drop_publications_with_short_titles_and_empty_authors(file):
    json_content = []
    with open(file, "r") as file_handle, open("drop_publications_with_short_titles.json", "w") as file_out:
        json_data = json.load(file_handle)
        #print(len(json_data))
        for item in json_data:
            splitted_array = item["title"].split()
            if len(splitted_array) > 1 or len(item["authors"] > 0):
                json_content.append(item)
            else:
                pass
        json.dump(json_content,file_out)

def fix_issn_with_doi(file):
    json_content = []
    pattern = "[A-z]"
    check_list = ["issn","doi"]
    with open(file, "r") as file_handle, open("fix_issn_with_doi.json", "w") as file_out:
        json_data = json.load(file_handle)
        for item in json_data:
            if "issn" in item and "doi" in item  and re.match(pattern, item["issn"]): #TODO refactor this PLEASE
                item["issn"] = item["doi"] #if "doi" in item or item["doi"] != "" else ""
            json_content.append(item)
        json.dump(json_content,file_out)
    
def fix_publication_type(file):
    json_content = []
    check_list = ["@"]
    with open(file, "r") as file_handle, open("fix_publication_type.json", "w") as file_out:
        json_data = json.load(file_handle)
        for item in json_data:
        # print(item["venue"]["raw"])
            if "doc_type" not in item:
                if  "venue" in item and "raw" in item["venue"] and "@" in item["venue"]["raw"]:
                    #print(item["venue"]["raw"])
                    item["doc_type"] = "Workshop"
                elif ("volume" in item and len(item["volume"]) > 0) or ("issue" in item and len(item["issue"]) > 0):
                    item["doc_type"] = "Journal publication"
                else: 
                    item["doc_type"] = "Conference paper"
            json_content.append(item)
        json.dump(json_content,file_out)


def refining_venues(file):
    json_content = []
    with open(file, "r") as file_handle, open("refined_venues.json", "w") as file_out:
        json_data = json.load(file_handle)
        for item in json_data:
            if "venue" in item and "raw" in item["venue"]: #TODO refactor this PLEASE
                venue = item["venue"] 
                venue_raw = venue["raw"]
                # print(item["venue"]["raw"])
                # print("================== \n")
                if venue_raw != None and (len(venue_raw) < 6 or len(venue_raw.split()) < 2):
                    response = requests.get(f"https://dblp.org/search/venue/api?q={venue_raw}&format=json")
                    if response.status_code == 200:
                        result = response.json()
                        if result["result"]["hits"] and "hit" in result["result"]["hits"] and result["result"]["hits"]["hit"][0]["info"]["venue"]:
                            item["venue"]["name"] = result["result"]["hits"]["hit"][0]["info"]["venue"]
                        else: 
                            item["venue"]["name"] = venue_raw
                    else:
                        item["venue"]["name"] = venue_raw
                else: 
                    item["venue"]["name"] = venue_raw
            
            json_content.append(item)
        json.dump(json_content,file_out)




#input_file = "input/staging_data.json"
#output_file = "output/staging_data.json"

input_file = "drop_publications_with_short_titles.json"

refining_venues(input_file)

#fix_json(input_file,output_file) # always replace [] after runing
#drop_publications_with_short_titles(output_file)
#fix_issn_with_doi(input_file)
#fix_publication_type(input_file)
 #fix_json | remove_number | drop_publications_with

