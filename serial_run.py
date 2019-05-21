#!/usr/bin/env python
# coding: utf-8

'''
A script to automate the up-to date puling of the FAO dataset. 
http://www.fao.org/faostat/en/#home

For issues contact: daniel.ellis@sei.org


This script assumes you have enough memory to download each required files. 
Intended for python 2 ( this is shipped with linux by default ) - but should also run on python3 (untested)

Full download took 508 seconds in serial.
'''


###############################################################################################################
__version__ = '0.0.1'
__url__ = 'http://fenixservices.fao.org/faostat/static/bulkdownloads/datasets_E.json'
__location__ = "\\\\storage.its.york.ac.uk\sei\SEI-Y RESEARCH GROUPS\SCP Group\SHARED RESOURCES\FAOSTAT_DATA\\"

import json, os, re, requests, zipfile, io, tempfile, shutil,glob, difflib,warnings ,copy, time,urllib
from datetime import datetime

verbose=False

renm = re.compile(r'\s+')
dirs = re.compile(r'[:-]')

###############################################################################################################

def get_latest():
    '''
    A function to get the latest descriptive json from the file
    '''
    global __url__
    response = urllib.urlopen(__url__)
    data = json.loads(response.read().decode('latin-1').strip())
    #print(json.dumps(data, indent=4, sort_keys=True))

    js = data['Datasets'][u'Dataset']
    
    return dict(zip(map( lambda x : x[u'DatasetName'], js) , js))


def savejson(jsdata, filename = 'latest.json'):
    global __location__
    with open(__location__ + filename,'w') as f:
        f.write(json.dumps(jsdata, indent=4, sort_keys=True))


###############################################################################################################
# Main body
###############################################################################################################

latest = get_latest()

#Check that the final destination is correct and search for json dataset
try:
    current = json.load(open(__location__ + 'latest.json'))
except IOError:
    if os.path.isdir(__location__):
        # the general directory exists but is new... 
        print ('creating new reppository')
        current = copy.deepcopy(latest)
        for i in current:
            current[i]['DateUpdate']='No Date.'
    else:
        raise('You have specified an incorrect location',__location__)
            


###############################################################################################################


# Check if anything has been updated

start_time = time.time()


needs_update = []
d_url=''

mainlog = open(__location__+"changes.log", "a")
mainlog.write("\n\n############ %s ############\n\n"%datetime.now().strftime('%Y-%m-%d'))
            

for item,dataset in enumerate(latest):
    #print (current[dataset]['DateUpdate'], latest[dataset]['DateUpdate'])
    try:
        if current[dataset]['DateUpdate'] != latest[dataset]['DateUpdate']:

            # get download link
            d_url = latest[dataset][u'FileLocation']
            ftype = latest[dataset][u'FileType']
            name_full = latest[dataset][u'DatasetName'].decode('latin-1')
            # file location...
            nsplit = [renm.sub('_',x.strip()) for x in dirs.split(name_full)]
            dirchain = '/'.join(list(nsplit[:-1]))
            name = nsplit[-1]+'.%s'%ftype
            final_loc = __location__+dirchain+'/%s'%(name)
            dirpath = tempfile.mkdtemp()   
            print ('Updating: ',name_full)


            #make directory if it does not exist
            if not os.path.isdir(__location__+dirchain):       
                os.makedirs(__location__+dirchain)

            #local logfile
            plog = open(__location__+dirchain+'/%s'%"diff.log", "a")
            plog.write("\n############ %s-%s ############\n"%(datetime.now().strftime('%Y-%m-%d'),nsplit[-1]))
            
            # Download file to temporary folder
            try:
                r = requests.get(d_url)
                z = zipfile.ZipFile(io.BytesIO(r.content))
                z.testzip()
                z.extractall(dirpath)
            except NotImplementedError:
                print 'NotImplementedError: compression type 9 (deflate64) - not unzipping'
                plog.write('\n Proprietry format: compression type 9 (deflate64) - not unzipping: '+nsplit[-1])
                urllib.urlretrieve(d_url, filename=__location__+dirchain+'/%s.zip'%nsplit[-1])
                mainlog.write('Proprietry format - not unzipping: %s - %s\n'%(name_full,final_loc) )
                plog.close()
                shutil.rmtree(dirpath)
                print ('%d %s - %d seconds (elapsed) '%((float(item)+1)/len(latest)*100, '%', (time.time() - start_time)))
                continue
                
                

            if verbose: print (dirpath,'->',final_loc) #, os.listdir(dirpath)
            files = glob.glob(dirpath+'\\*.%s'%ftype)
            if len(files) >1: 
                warnings.warn("Warning: More than one file detected for %s. Only the first has been used."%name)

         
            #read the updated file
            new = open(files[0],'r').readlines()

            if os.path.exists(final_loc):
                    old = open(final_loc,'r').readlines()
                    for line in difflib.unified_diff(new, old, fromfile=
    datetime.now().strftime('%H:%M:%S')+'_new', tofile='%s_old'%name, lineterm=''):
                        plog.write(line)
                    mainlog.write('Updating: %s - %s\n'%(name_full,final_loc) )
            else:
                plog.write('\n Created '+name)
                mainlog.write('Adding: %s - %s\n'%(name_full,final_loc) )


            
            plog.close()

            #move the new file
            shutil.move(files[0], final_loc)

            #rm temp dir
            shutil.rmtree(dirpath)
            
            print ('%d %s - %d seconds (elapsed) '%((float(item)+1)/len(latest)*100, '%', (time.time() - start_time)))

    except NameError:
            # for a new dataset in an existing directory
            print ('Adding new dataset!: ', dataset)

            # get download link
            d_url = latest[dataset][u'FileLocation']
            nsplit = [renm.sub('_',x.strip()) for x in dirs.split(latest[dataset][u'DatasetName'].decode('latin-1'))]
            dirchain = '/'.join(list(nsplit[:-1]))
            name = nsplit[-1]+'.%s'%latest[dataset][u'FileType']
            final_loc = __location__+dirchain+'/%s'%(name)
            dirpath = tempfile.mkdtemp()
 
            if not os.path.isdir(__location__+dirchain):os.makedirs(__location__+dirchain)
            
            
            try:zipfile.ZipFile(io.BytesIO(requests.get(d_url).content)).extractall(dirpath)
            except NotImplementedError:
                plog.write('\n Proprietry format: compression type 9 (deflate64) - not unzipping: '+nsplit[-1])
                urllib.urlretrieve(d_url, filename=__location__+dirchain+'/%s.zip'%nsplit[-1])
                mainlog.write('Proprietry format - not unzipping: %s - %s\n'%(name_full,final_loc) )
                plog.close()
                shutil.rmtree(dirpath)
                continue
            
            
            files = glob.glob(dirpath+'\\*.%s'%ftype)
            if len(files) >1: warnings.warn("Warning: More than one file detected for %s. Only the first has been used."%name)

            mainlog.write('Adding: %s - %s\n'%(name_full,final_loc) )
            with open(__location__+dirchain+'/%s'%'diff.log', "a") as plog:
                plog.write("\n############ %s ############\n"%datetime.now().strftime('%Y-%m-%d'))
                plog.write('\n Created.')
                
                
            #move the new file
            shutil.move(files[0], final_loc)
            #rm temp dir
            shutil.rmtree(dirpath)           
         

mainlog.close()
#update saved json descriptor file
savejson(latest)
print ('Finished')
